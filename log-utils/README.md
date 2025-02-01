**Utils monorepo: Log Utils**
==================================

Just some Python logging utils.


Usage
=====

---

See top docstring in [log_adapter.py](log_utils/log_adapter.py).


Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "log-utils @ ../log-utils"
    # "log-utils @ file:///Users/myuser/workspace/utils-monorepo/log-utils"
    # Or, to install the extras:
    # "log-utils[rich-adapter] @ ../log-utils"
    # "log-utils[loguru-adapter] @ ../log-utils"
    # "log-utils[powertools-adapter] @ ../log-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
log-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "log-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils",
    # Or, to install the extras:
    # "log-utils[rich-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
    # "log-utils[loguru-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
    # "log-utils[powertools-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
]
```

Pip install
-----------
```sh
$ pip install "log-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
# Or, to install the extras:
$ pip install "log-utils[rich-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
$ pip install "log-utils[loguru-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
$ pip install "log-utils[powertools-adapter] @ git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
