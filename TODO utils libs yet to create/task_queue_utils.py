"""
Task queue based on threads and implemented with ThreadPoolExecutor.
Based on the example in the docs: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example

TODO see tests in map-cli.
"""

import concurrent.futures
import itertools
import logging
import os
import threading
import traceback
from queue import Queue
from typing import Callable, Iterable, Optional

from . import fqn

# Src:
#  - Python 3.9: https://github.com/python/cpython/blob/b06c3b364720ce8e8dfb74dfa24434e067ac89ba/Lib/concurrent/futures/thread.py#L142
#  - Python 3.13: https://github.com/python/cpython/blob/329865b883c4c51026c6abe656f2c0e83fed2c4e/Lib/concurrent/futures/thread.py#L146
MAX_CONCURRENT_THREADS = min(32, (os.cpu_count() or 1) + 4)


# TODO dataclasses are a good fit for this, but available only from Python 3.7+.
class CallArgs:
    # Note: using a dict in place of this class does not have any effect on time/space
    # performance.
    def __init__(
        self, args=(), kwargs: Optional[dict] = None, task_id: Optional[str] = None
    ):
        self.args = args
        if kwargs is None:
            kwargs = {}
        self.kwargs = kwargs
        ## This is time consuming, which is relevant when we need to generate many CallArgs.
        # if task_id is None:
        #     task_id = str(uuid.uuid4())
        self.task_id = task_id


class TaskError(Exception):
    def __init__(self, future: concurrent.futures.Future, task_id: str):
        super().__init__(f"Task failed: id={task_id}")
        self.future = future
        self.task_id = task_id


class TaskQueue:
    """
    A classic task queue for the concurrent execution of tasks using threads.
    Tasks results and exceptions are collected.

    Example:
        def add(a, b, c=0):
            return a + b + c

        def yield_call_args_fn():
            yield CallArgs(args=(0, 1))
            yield CallArgs(args=(0, 1), kwargs=dict(c=1))

        call_args = (
            CallArgs(args=(0, 3)),
            CallArgs(args=(0, 3), kwargs=dict(c=1)),
        )

        q = TaskQueue(fn=add, call_args=args, yield_call_args_fn=yield_call_args_fn)

        # for result, task_id in q.yield_results():
        #     print(f"{task_id} result: {result}")
        results = [res for res, task_id in q.yield_results()]
        results.sort()
        assert results == [1, 2, 3, 4]

    Note: check the tests for more examples and analysis on performance.
    """

    def __init__(
        self,
        fn: Callable,
        call_args: Iterable[CallArgs] = (),
        yield_call_args_fn: Optional[Callable] = None,
        max_workers: Optional[int] = None,
        overall_timeout: Optional[float] = None,
    ):
        """
        Args:
            fn: the task function, all submitted tasks executes this function.
            call_args: collection (list) of `CallArgs`, each of them is submitted to
             a new task (chained with `yield_call_args_fn`).
            yield_call_args_fn: generator function to yield `CallArgs`, each of them is
            submitted to a new task (chained with `call_args`).
            max_workers: max numbers of workers, thus concurrent threads.
            overall_timeout (seconds): timeout for the time taken to complete all the
             submitted tasks (not just one). When the timout happens, a TimeoutError
             is raised, but:
                - the future that caused the timout is not interrupted
                - the scheduled futures are not cancelled.
             This behavior makes the timeout feature almost useless.
             This behavior is intentional as a timeout should be better handled in the
             submitted task itself with a hard timout on a network call for instance.
        """
        self.fn = fn
        self.yield_call_args_iter = iter(call_args)
        self.yield_call_args_fn = yield_call_args_fn
        if yield_call_args_fn:
            self.yield_call_args_iter = itertools.chain(call_args, yield_call_args_fn())
        if max_workers is None:
            max_workers = MAX_CONCURRENT_THREADS
        self.max_workers = max_workers
        self.overall_timeout = overall_timeout
        self.thread_name_prefix = "TaskQueue-" + fqn.get_fqn(fn)

    def yield_results(self, do_ignore_exceptions=False):
        # Note: this code can be easily extended to support ProcessPoolExecutor.
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers, thread_name_prefix=self.thread_name_prefix
        ) as executor:
            futures = (
                {}
            )  # Using a dict here does not make if faster nor less memory-eager.
            for param in self.yield_call_args_iter:
                future = executor.submit(self.fn, *param.args, **param.kwargs)
                futures[future] = param.task_id

            for future in concurrent.futures.as_completed(
                futures, timeout=self.overall_timeout
            ):
                task_id = futures[future]
                try:
                    yield future.result(), task_id
                except Exception as exc:
                    if do_ignore_exceptions:
                        continue
                    for f_to_cancel in futures:
                        f_to_cancel.cancel()
                    raise TaskError(future=future, task_id=task_id) from exc

    ## Using `executor.map` instead of `concurrent.futures.as_completed` does not affect much performance.
    # def yield_results(self):
    #     with concurrent.futures.ThreadPoolExecutor(
    #         max_workers=self.max_workers, thread_name_prefix=self.thread_name_prefix
    #     ) as executor:
    #         for result in executor.map(lambda p: self.fn(*p.args, *p.kwargs), self.yield_call_args_fn()):
    #             yield result


class SimpleTaskQueue:
    """
    An alternative version of a task queue, compared to `TaskQueue`. It is sometimes more performant (in time and space),
    but with relevant limitations.
    Due to these limitation, `TaskQueue` is often a better choice than `SimpleTaskQueue`.
    Limitations:
    - results (of the submitted tasks) are not collected.
    - exceptions are ignored, so there is no way to know if a task failed.
    Note that both these features could be added, but then the performance would be comparable to `TaskQueue` (which
    implements exactly those features).

    Note: check the tests for an analysis on performance.
    """

    def __init__(
        self,
        fn: Callable,
        yield_call_args_fn: Optional[Callable] = None,
        max_workers: Optional[int] = None,
    ):
        if max_workers is None:
            max_workers = MAX_CONCURRENT_THREADS
        self.max_workers = max_workers
        self.q: Queue = Queue()
        self.fn = fn
        self.yield_call_args_fn = yield_call_args_fn

    def submit(self):
        """
        Submit and start executing all tasks. Return when all tasks are completed (and ignore results and exceptions).
        """
        for _ in range(self.max_workers):
            thread_worker = threading.Thread(target=self._run_task)
            thread_worker.daemon = True
            thread_worker.start()
        for args in self.yield_call_args_fn():
            self.q.put(args)
        self.q.join()

    def _run_task(self):
        while True:
            call_args = self.q.get()
            if call_args is None:
                # `None` means to stop, thus propagating the stop to the other threads.
                self.q.put(None)
                # And finally stopping.
                return
            try:
                # task_args = param.args", ())
                # task_kwargs = param.get("kwargs", {})
                self.fn(*call_args.args, **call_args.kwargs)
            except Exception:
                # Print the traceback, but ignore the error and continue processing the
                # next task.
                logging.exception(traceback.format_exc())
                ## We might consider changing this behavior and stop the processing of the
                ## tasks early, but in that case using `TaskQueue` would be a better choice.
                # self.q.put(None)
                # return
            finally:
                self.q.task_done()
