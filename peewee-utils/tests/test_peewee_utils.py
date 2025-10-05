from datetime import datetime, timedelta, timezone

import peewee

import peewee_utils


def _now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


class MyActivityModel(peewee_utils.BasePeeweeModel):
    # The `id` would be implicitly added even of we comment this line, as we did
    #  not specify a primary key.
    id: int = peewee.AutoField()
    created_at: datetime = peewee_utils.UtcDateTimeField(default=_now_utc)
    # See trigger `update_activity_updated_at_after_update_on_activity` defined later.
    # Mind that you have to reload the model to get a fresh value for `updated_at`.
    updated_at: datetime = peewee_utils.UtcDateTimeField(default=_now_utc)
    name: str = peewee.CharField(max_length=512)


# Register all tables.
peewee_utils.register_tables(MyActivityModel)

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

# Register a trigger to update MyActivityModel.updated_at on every update.
# Update trigger: https://stackoverflow.com/questions/30780722/sqlite-and-recursive-triggers
# STRFTIME for timestamp with milliseconds: https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
peewee_utils.register_trigger(
    """
CREATE TRIGGER IF NOT EXISTS update_activity_updated_at_after_update_on_activity
AFTER UPDATE ON my_activity
FOR EACH ROW
WHEN (SELECT are_updated_at_triggers_enabled()) = 1
BEGIN
    UPDATE my_activity
    SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW');
END;
"""
)

# At last, configure.
peewee_utils.configure(get_sqlite_db_path_fn=lambda: ":memory:")


def _add_rows():
    a0 = MyActivityModel.create(name="one")
    a1 = MyActivityModel.create(name="two")
    return a0, a1


# To know how to properly test a project with Peewee and Sqlite, with db isolation
#  for single test, see sqlite-full-text-search in experiments-monorepo.
class Test:
    # `do_force_new_db_init` is useful in tests, when running concurrent tests with
    #   in-memory SQLite db.
    @peewee_utils.use_db(do_force_new_db_init=True)
    def test_happy_flow_decorator(self):
        _add_rows()
        assert MyActivityModel.select().count() == 2

    def test_happy_flow_ctx_manager(self):
        with peewee_utils.use_db(do_force_new_db_init=True):
            _add_rows()
            assert MyActivityModel.select().count() == 2

    # `do_force_new_db_init` is useful in tests, when running concurrent tests with
    #   in-memory SQLite db.
    @peewee_utils.use_db(do_force_new_db_init=True)
    def test_updated_at(self):
        _add_rows()
        # The goal is to ensure that when updating an MyActivityModel, then its `updated_at`
        #  attribute is automatically updated.
        a = MyActivityModel.get_by_id(1)
        assert a.created_at.tzinfo == timezone.utc
        assert a.updated_at > a.created_at
        assert (a.updated_at - a.created_at) > timedelta(seconds=0)
        assert (a.updated_at - a.created_at) < timedelta(seconds=1)

        prev_updated_at = a.updated_at
        a.name = "onebis"
        a.save()
        # Reload the model to get the new updated_at.
        a = MyActivityModel.get_by_id(1)
        assert a.updated_at > prev_updated_at
        assert (a.updated_at - prev_updated_at) > timedelta(seconds=0)
        assert (a.updated_at - prev_updated_at) < timedelta(seconds=1)
