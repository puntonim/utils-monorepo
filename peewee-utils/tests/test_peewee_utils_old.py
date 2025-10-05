from datetime import datetime, timedelta, timezone

import peewee

from peewee_utils import peewee_models_utils_old, peewee_utils_old


def _now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)


class ActivityModel(peewee_models_utils_old.BasePeeweeModel):
    # The `id` would be implicitly added even of we comment this line, as we did
    #  not specify a primary key.
    id: int = peewee.AutoField()
    created_at: datetime = peewee_models_utils_old.UtcDateTimeField(default=_now_utc)
    # See trigger `update_activity_updated_at_after_update_on_activity` defined later.
    # Mind that you have to reload the model to get a fresh value for `updated_at`.
    updated_at: datetime = peewee_models_utils_old.UtcDateTimeField(default=_now_utc)
    name: str = peewee.CharField(max_length=512)


def _create_models():
    # Register all tables.
    peewee_utils_old.register_tables(ActivityModel)

    # Add a custom SQL function that serves as feature toggle for the updated_at triggers.
    #  It returns 1 (True) always and it's invoked by every updated_at trigger.
    #  We can overwrite this function to return 0 in order to temp disable triggers.
    #  See tests/testfactories/domains/exercise_domain_factory.py.
    UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME = "are_updated_at_triggers_enabled"
    peewee_utils_old.register_sql_function(
        lambda: 1,
        UPDATED_AT_TRIGGERS_TOGGLE_FUNCTION_NAME,
        0,
    )

    # Register a trigger to update ActivityModel.updated_at on every update.
    # Update trigger: https://stackoverflow.com/questions/30780722/sqlite-and-recursive-triggers
    # STRFTIME for timestamp with milliseconds: https://stackoverflow.com/questions/17574784/sqlite-current-timestamp-with-milliseconds
    peewee_utils_old.register_trigger(
        """
    CREATE TRIGGER IF NOT EXISTS update_activity_updated_at_after_update_on_activity
    AFTER UPDATE ON activity_model
    FOR EACH ROW
    WHEN (SELECT are_updated_at_triggers_enabled()) = 1
    BEGIN
        UPDATE activity_model
        SET updated_at = STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW');
    END;
    """
    )

    # At last, configure peewee_utils_old.
    peewee_utils_old.configure(sqlite_db_path=":memory:")


@peewee_utils_old.use_db
def _add_rows():
    a0 = ActivityModel.create(name="one")
    a1 = ActivityModel.create(name="two")
    return a0, a1


class Test:
    def setup_method(self):
        _create_models()
        self.a0, self.a1 = _add_rows()

    @peewee_utils_old.use_db
    def test_happy_flow(self):
        assert ActivityModel.select().count() == 2

    @peewee_utils_old.use_db
    def test_updated_at(self):
        # The goal is to ensure that when updating an Activity, then its `updated_at`
        #  attribute is automatically updated.
        a = ActivityModel.get_by_id(1)
        assert a.created_at.tzinfo == timezone.utc
        assert a.updated_at > a.created_at
        assert (a.updated_at - a.created_at) > timedelta(seconds=0)
        assert (a.updated_at - a.created_at) < timedelta(seconds=1)

        prev_updated_at = a.updated_at
        a.name = "onebis"
        a.save()
        # Reload the model to get the new updated_at.
        a = ActivityModel.get_by_id(1)
        assert a.updated_at > prev_updated_at
        assert (a.updated_at - prev_updated_at) > timedelta(seconds=0)
        assert (a.updated_at - prev_updated_at) < timedelta(seconds=1)
