"""
** PEEWEE UTILS **
==================

*IMP: this is the **new** version of peewee-utils. The old version is in *_old.py.
I prefer not to use versioning in order to keep things simple.*

Used, among the others, in:
 - (GREAT EXAMPLE) https://github.com/puntonim/experiments-monorepo/tree/main/SQLITE%20FULL-TEXT%20SEARCH/sqlite-full-text-search-cli-exp

Models definition
-----------------
First, define models in a `data_models.py` file:
```py
from datetime import datetime
import datetime_utils
import peewee
import peewee_utils
from ..conf import settings

class ActivityModel(peewee_utils.BasePeeweeModel):
    # The `id` would be implicitly added even of we comment this line, as we did
    #  not specify a primary key.
    id: int = peewee.AutoField()
    created_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
    # See trigger `update_activity_updated_at_after_update_on_activity` defined later.
    # Mind that you have to reload the model to get a fresh value for `updated_at`.
    updated_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
    name: str = peewee.CharField(max_length=512)

# Register all tables.
peewee_utils.register_tables(ActivityModel)

# Add a custom SQL function that serves as feature toggle for the updated_at triggers.
#  It returns 1 (True) always and it's invoked by every updated_at trigger.
#  We can overwrite this function to return 0 in order to temp disable triggers.
#  See gymiq/tests/testfactories/domains/exercise_domain_factory.py.
UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME = "are_updated_at_triggers_enabled"
peewee_utils.register_sql_function(
    lambda: 1,
    UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME,
    0,
)

# Register a trigger to update ActivityModel.updated_at on every update.
# Update trigger: https://stackoverflow.com/questions/30780722/sqlite-and-recursive-triggers
# STRFTIME for timestamp with milliseconds: https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
peewee_utils.register_trigger(
    \""" <------ IMP: remove the \
CREATE TRIGGER IF NOT EXISTS update_activity_updated_at_after_update_on_activity
AFTER UPDATE ON activity
FOR EACH ROW
WHEN (SELECT are_updated_at_triggers_enabled()) = 1
BEGIN
    UPDATE activity
    SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW');
END;
\""" <------ IMP: remove the \
)

# At last, configure peewee_utils with the SQLite DB path.
# Using lambda functions, instead of actual values, for lazy init, which is necessary
#  when overriding settings in tests.
peewee_utils.configure(
    get_sqlite_db_path_fn=lambda: settings.DB_PATH,
    get_do_log_peewee_queries_fn=lambda: settings.DO_LOG_PEEWEE_QUERIES,
    get_load_extensions_fn=lambda: (settings.SQLITE_EXT_SNOWBALL_MACOS_PATH,),
)
```

Functions/methods that require access to DB
-------------------------------------------
First you need to create the DB, only once.
For instance, you can create a CLI admin command (or an admin endpoint) that runs:
(example: See for example: https://github.com/puntonim/experiments-monorepo/blob/main/SQLITE%20FULL-TEXT%20SEARCH/sqlite-full-text-search-cli-exp/fts_exp/views/admin/admin_db_create_cli_view.py)
```py
import peewee

peewee_utils.create_all_tables()
```

Then use the decorator and ctx manager `peewee_utils.use_db()` with any function/method
 or snippet that requires access to the DB:
```py
import peewee_utils

@peewee_utils.use_db()
def count():
    query = db_models.ActivityModel.select().where(db_models.ActivityModel.name == "myname")
    return query.count()

def count():
    with @peewee_utils.use_db():
        query = db_models.ActivityModel.select().where(db_models.ActivityModel.name == "myname")
        return query.count()
```

Tests
-----
See tests in sqlite-full-text-search-cli-exp in experiments-monorepo: https://github.com/puntonim/experiments-monorepo/tree/main/SQLITE%20FULL-TEXT%20SEARCH/sqlite-full-text-search-cli-exp/tests

In `conftest.py`:
```py
import peewee_utils
import pytest
import settings_utils
from fts_exp.conf.settings import settings, test_settings

@pytest.fixture(autouse=True, scope="function")
def test_settings_fixture(monkeypatch, request):
    # Copy all test settings to settings.
    settings_utils.copy_settings(test_settings, settings)

@pytest.fixture(autouse=True, scope="function")
def use_db_fixture(test_settings_fixture):
    # `do_force_new_db_init` is required when running concurrent tests with in-memory
    #  SQLite db.
    with peewee_utils.use_db(do_force_new_db_init=True):
        peewee_utils.create_all_tables()
        yield
```

Then write tests like this:
```py
class TestItemModel:
    def test_create(self):
        assert ItemModel.select().count() == 0
        ItemModel.create(title="My first title", notes="My first note")
        ItemModel.create(title="My second title", notes="My second note")
        assert ItemModel.select().count() == 2

    def test_db_isolation(self):
        # It's intentionally the same as the prev test. The purpose is to ensure that
        #  single tests isolation works and the 2 items inserted in the prev tests are
        #  gone.
        assert ItemModel.select().count() == 0
        ItemModel.create(title="My first title", notes="My first note")
        ItemModel.create(title="My second title", notes="My second note")
        assert ItemModel.select().count() == 2
```
"""

import functools
import sys
import uuid
from contextlib import ContextDecorator
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Sequence

import log_utils as logger
import peewee
from playhouse.db_url import connect
from playhouse.pool import PooledSqliteDatabase

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "configure",
    "get_db",
    "create_all_tables",
    "drop_all_tables",
    "use_db",
    "serialize_to_sqlite",
    "register_tables",
    "register_trigger",
    "register_sql_function",
    "print_compile_options",
]

_TABLE_MODELS = []
_TRIGGERS_SQL = []
_SQL_FUNCTIONS = []

_CONFIG = {
    "get_sqlite_db_path_fn": lambda: ":memory:",
    "get_do_log_peewee_queries_fn": lambda: False,
    "get_load_extensions_fn": lambda: None,
}

_DATABASE_PROXY = peewee.DatabaseProxy()
_DB: PooledSqliteDatabase | None = None


def configure(
    get_sqlite_db_path_fn: Callable[[], str] = lambda: ":memory:",
    get_do_log_peewee_queries_fn: Callable[[], bool] = lambda: False,
    get_load_extensions_fn: Callable[[], Sequence[str | Path] | None] = lambda: None,
):
    _CONFIG["get_sqlite_db_path_fn"] = get_sqlite_db_path_fn
    _CONFIG["get_do_log_peewee_queries_fn"] = get_do_log_peewee_queries_fn
    _CONFIG["get_load_extensions_fn"] = get_load_extensions_fn


def get_db(do_force_new_db_init: bool = False) -> PooledSqliteDatabase:
    """
    Get the db connection, an instance of PooledSqliteDatabase.

    Args:
        do_force_new_db_init: useful in tests, when running concurrent tests with
         in-memory SQLite db. See sqlite-full-test-search in experiments-monorepo.
    """
    # Lazy init of the db connection.
    # The lazy init is useful, for examples, when overriding settings in tests.
    if _DB is None or do_force_new_db_init:
        _db_init()
    return _DB


def _db_init():
    sqlite_db_path = _CONFIG["get_sqlite_db_path_fn"]()
    # Note: sqlite_db_path gets stored in `db.database`.
    logger.info(f"Using DB {sqlite_db_path} ...")

    # Log to stderr if the fn get_do_log_peewee_queries_fn() passed in the config()
    #  returns true.
    get_do_log_peewee_queries_fn = _CONFIG["get_do_log_peewee_queries_fn"]
    if get_do_log_peewee_queries_fn():
        # Log all queries to stderr.
        # Doc: https://docs.peewee-orm.com/en/latest/peewee/database.html#logging-queries
        import logging

        peewee_logger = logging.getLogger("peewee")
        peewee_logger.addHandler(logging.StreamHandler())
        peewee_logger.setLevel(logging.DEBUG)

    # Use PRAGMA foreign_keys to enforce foreign-key constraints to avoid being able to
    #  insert a row with a foreign key ID that does not exist.
    #  Example: Pet.create(owner=99, name="Spino", animal_type="dog") where 99 does not exist.
    # Use a connection pool, the pool is useful for subsequent function invocations (AWS Lambda).
    #  Docs: https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#connection-pool
    #  Max 10 connection in the pool.
    #  A connection is disposed 300 sec (5 min) after being closed.
    pool_config = "?max_connections=10&stale_timeout=300"
    # Using `connect()` instead of `PooledSqliteDatabase` makes it easier to use a setting
    #  for prod and test to use diff databases (eg. SQLite and PostgreSQL). For the same
    #  use case, you can also use a proxy:
    #  https://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database
    global _DB
    _DB = connect(  # PooledSqliteDatabase.
        f"sqlite+pool:///{sqlite_db_path}{pool_config}",
        # Disable PRAGMA `recursive_triggers` because we defined a trigger to handle
        #  `updated_at` (btw the default value is OFF).
        pragmas={"foreign_keys": "ON", "recursive_triggers": "OFF"},
        autoconnect=False,  # Best practice.
    )
    _DATABASE_PROXY.initialize(_DB)

    # Load SQLite extensions.
    for ext in _CONFIG["get_load_extensions_fn"]() or tuple():
        ext: str | Path
        _load_sqlite_extension(_DB, ext)


def _load_sqlite_extension(_db, path: str | Path):
    """
    Load a loadable extension into SQLite.

    The extension should have been compiled for the current architecture (eg. macos).
    And SQLite should have been compiled with the loadable extensions enabled.
    See notes in my laptop in _SW, SYS ENGINEERING/DB, NOSQL (PostgreSQL, Redis, MongoDB, ...)/SQLite/SQLite extensions and compile options.md.
    """
    try:
        _db.enable_load_extension(True)
    except AttributeError:
        pass
    _db.load_extension(str(path))


def create_all_tables():
    """
    Create all tables, if they don't exist already. Safe to call on every app bootstrap.
    In a real-case project use migrations instead:
     https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations
    """
    db = get_db()

    # Open the connection.
    logger.info("Opening DB connection")
    db.connect(reuse_if_open=True)

    # Create tables. In a real-case project use migrations instead:
    #  https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations
    logger.info("Creating tables")
    db.create_tables(_TABLE_MODELS)

    # Create SQL functions.
    logger.info("Creating SQL functions")
    for sql_function_args in _SQL_FUNCTIONS:
        db.register_function(
            *sql_function_args,
        )

    # Create triggers.
    logger.info("Creating triggers")
    for sql in _TRIGGERS_SQL:
        db.execute_sql(sql)


def drop_all_tables():
    db = get_db()

    # Open the connection.
    logger.info("Opening DB connection")
    db.connect(reuse_if_open=True)

    logger.info("Dropping tables")
    # Temporary disable the FOREIGN KEY constraint check in order to avoid errors when
    #  dropping tables with ForeignKeys.
    db.execute_sql("PRAGMA foreign_keys = OFF;")
    db.drop_tables(_TABLE_MODELS)
    db.execute_sql("PRAGMA foreign_keys = ON;")


# Note: decorator to be used with ().
class use_db(ContextDecorator):
    """
    Context manager and decorator.

    Examples:
        import peewee_utils

        @peewee_utils.use_db()  <-- as decorator.
        def count():
            query = db_models.ActivityModel.select().where(db_models.ActivityModel.name == "myname")
            return query.count()

        def count():
            with @peewee_utils.use_db():  <-- as ctx manager.
                query = db_models.ActivityModel.select().where(db_models.ActivityModel.name == "myname")
                return query.count()
    """

    def __init__(self, do_force_new_db_init: bool = False):
        """
        Args:
            do_force_new_db_init: useful in tests, when running concurrent tests with
             in-memory SQLite db. See sqlite-full-text-search in experiments-monorepo.
        """
        self.do_force_new_db_init = do_force_new_db_init
        self.db = None

    def __enter__(self):
        self.db = get_db(do_force_new_db_init=self.do_force_new_db_init)
        self.was_already_open = False if self.db.is_closed() else True
        self.db.connect(reuse_if_open=True)
        return self

    def __exit__(self, *exc):
        # Consider closing the connection only if it wasn't already open, so it was
        #  this code that actually opened the connection.
        if not self.was_already_open:
            # Close the connection to the DB.
            # Do not close it here in test (check `conftest.py` instead).
            if not self.db.is_closed():
                logger.info("Closing DB connection")
                self.db.close()
        return False


def serialize_to_sqlite(obj: Any) -> Any:
    """
    Convert any object to a valid Peewee SQLite value format.

    Examples
        datetime.datetime(2022, 5, 24, 10, 11, 12, 123456, tzinfo=datetime.timezone.utc) > "2022-05-24T10:11:12.123456+00:00"
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, Enum):
        return obj.value
    return obj


# To check all compile options (including the enabled extensions) in SQLite:
#   https://stackoverflow.com/questions/36655777/python-and-sqlite3-check-if-i-can-use-fts5-extension/36663390#36663390
def print_compile_options():
    """
    Debug function to print all compile options (including the enabled stock
     extensions like FTS5 and the loading extensions status) in SQLite:
    """
    db = get_db()
    sql = "pragma compile_options;"
    cursor = db.execute_sql(sql)
    for row in cursor.fetchall():
        print(row)


def register_tables(*models):
    for model in models:
        _TABLE_MODELS.append(model)


def register_trigger(sql):
    _TRIGGERS_SQL.append(sql)


def register_sql_function(fn, name, num_params):
    # Docs: https://www.sqlite.org/appfunc.html
    _SQL_FUNCTIONS.append((fn, name, num_params))
