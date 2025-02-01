"""
** PEEWEE UTILS **
==================

Used, among the others, in:
 - strava-monorepo/projects/strava-exporter-to-db: a simple CLI (without any
    CLI framework).

Models definition
-----------------
First, define models in a `data_models.py` file:
```py
from datetime import datetime

import datetime_utils
import peewee
import peewee_utils

from ..conf import settings


class Activity(peewee_utils.BasePeeweeModel):
    # The `id` would be implicitly added even of we comment this line, as we did
    #  not specify a primary key.
    id: int = peewee.AutoField()
    created_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
    # See trigger `update_activity_updated_at_after_update_on_activity` defined later.
    # Mind that you have to reload the model to get a fresh value for `updated_at`.
    updated_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
    name: str = peewee.CharField(max_length=512)


# Register all tables.
peewee_utils.register_tables(Activity)

# Add a custom SQL function that serves as feature toggle for the updated_at triggers.
#  It returns 1 (True) always and it's invoked by every updated_at trigger.
#  We can overwrite this function to return 0 in order to temp disable triggers.
#  See tests/testfactories/domains/exercise_domain_factory.py.
UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME = "are_updated_at_triggers_enabled"
peewee_utils.register_sql_function(
    lambda: 1,
    UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME,
    0,
)

# Register a trigger to update Activity.updated_at on every update.
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

# At last, configure peewee_utils.
peewee_utils.configure(db_path=settings.DB_PATH)
```

Functions/methods that require access to DB
-------------------------------------------
Then decorate with `@peewee_utils.use_db` any function/method that requires access
 to the DB:
```py
import peewee_utils
from .importer_from_strava_api_to_db import db_models

@peewee_utils.use_db
def main():
    query = db_models.Activity.select().where(db_models.Activity.name == "myname")
    assert query.count() == 1
```
"""

import functools
import sys
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

import log_utils as logger
import peewee
from playhouse.db_url import connect
from playhouse.pool import PooledSqliteDatabase

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "configure",
    "db",
    "create_all_tables",
    "drop_all_tables",
    "use_db",
    "serialize_to_sqlite",
    "register_tables",
    "register_trigger",
    "register_sql_function",
]

_TABLE_MODELS = []
_TRIGGERS_SQL = []
_SQL_FUNCTIONS = []

_CONFIG = {
    "db_path": ":memory:",
    "do_log_peewee_queries": False,
}


def configure(db_path: str = ":memory:", do_log_peewee_queries: bool = False):
    global _CONFIG
    _CONFIG["db_path"] = db_path
    _CONFIG["do_log_peewee_queries"] = do_log_peewee_queries

    if do_log_peewee_queries:
        # Log all queries to stderr.
        # Doc: https://docs.peewee-orm.com/en/latest/peewee/database.html#logging-queries

        import logging

        peewee_logger = logging.getLogger("peewee")
        peewee_logger.addHandler(logging.StreamHandler())
        peewee_logger.setLevel(logging.DEBUG)


_database_proxy = peewee.DatabaseProxy()
# `db` is lazily computed, see `__getattr__()`.
db: PooledSqliteDatabase | None = None


def __getattr__(name: str) -> Any:
    # Lazy init of the `db` module var: https://stackoverflow.com/a/52359211.
    # From Python docs: """The __getattr__ function at the module level should accept
    #  one argument which is the name of an attribute and return the computed value or
    #  raise an AttributeError. If an attribute is not found on a module object through
    #  the normal lookup, i.e. object.__getattribute__(), then __getattr__ is searched
    #  in the module __dict__ before raising an AttributeError."""

    if name == "db":
        if db is None:
            _db_init()
        return db
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def _db_init():
    global _CONFIG
    db_path = _CONFIG["db_path"]
    # Note: db_path gets stored in `db.database`.
    logger.info(f"Using DB {db_path} ...")

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
    global db
    db = connect(
        f"sqlite+pool:///{db_path}{pool_config}",
        # Disable PRAGMA `recursive_triggers` because we defined a trigger to handle
        #  `updated_at` (btw the default value is OFF).
        pragmas={"foreign_keys": "ON", "recursive_triggers": "OFF"},
        autoconnect=False,  # Best practice.
    )
    _database_proxy.initialize(db)


def create_all_tables():
    """
    Create all tables, if they don't exist already. Safe to call on every app bootstrap.
    In a real-case project use migrations instead:
     https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations
    """
    # Trick to invoke the lazy init of `db` within this module.
    db = __getattr__("db")

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
    # Trick to invoke the lazy init of `db` within this module.
    db = __getattr__("db")

    # Open the connection.
    logger.info("Opening DB connection")
    db.connect(reuse_if_open=True)

    logger.info("Dropping tables")
    # Temporary disable the FOREIGN KEY constraint check in order to avoid errors when
    #  dropping tables with ForeignKeys.
    db.execute_sql("PRAGMA foreign_keys = OFF;")
    db.drop_tables(_TABLE_MODELS)
    db.execute_sql("PRAGMA foreign_keys = ON;")


def use_db(fn):
    @functools.wraps(fn)
    def closure(*fn_args, **fn_kwargs):
        # Open DB connection and create all tables.
        # db.connect(reuse_if_open=True)  # Opened by `create_all_tables()`.
        create_all_tables()

        # Invoke original function.
        return_value = fn(*fn_args, **fn_kwargs)

        # Trick to invoke the lazy init of `db` within this module.
        db = __getattr__("db")
        # Close the connection to the DB.
        # Do not close it here in test (check `conftest.py` instead).
        if not db.is_closed() and not "pytest" in sys.modules:
            logger.info("Closing DB connection")
            db.close()

        return return_value

    return closure


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


def register_tables(*models):
    for model in models:
        _TABLE_MODELS.append(model)


def register_trigger(sql):
    _TRIGGERS_SQL.append(sql)


def register_sql_function(fn, name, num_params):
    # Docs: https://www.sqlite.org/appfunc.html
    _SQL_FUNCTIONS.append((fn, name, num_params))
