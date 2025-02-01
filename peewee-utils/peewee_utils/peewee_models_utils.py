from datetime import datetime, timezone
from typing import get_type_hints

import peewee

from .peewee_utils import _database_proxy

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "BasePeeweeModel",
    "NotADatetime",
    "NaiveDatetime",
    "UtcDateTimeField",
]


class IntrospectablePeeweeModel:
    def to_dict(self) -> dict:
        return self.__data__

    @classmethod
    def get_fields(cls) -> dict:
        return cls._meta.fields

    @classmethod
    def get_annotations(cls):
        return get_type_hints(cls)  # Or: cls.__annotations__.


class BasePeeweeModel(peewee.Model, IntrospectablePeeweeModel):
    class Meta:
        database = _database_proxy
        # `legacy_table_names` defaults to False as of Peewee 4.0.
        # https://docs.peewee-orm.com/en/latest/peewee/models.html#table-names
        legacy_table_names = False


class BaseUtcDateTimeFieldException(Exception):
    pass


class NotADatetime(BaseUtcDateTimeFieldException):
    pass


class NaiveDatetime(BaseUtcDateTimeFieldException):
    def __init__(self, message="Naive datetime not accepted"):
        super().__init__(message)


class UtcDateTimeField(peewee.DateTimeField):
    """
    DateTime timestamp must be stored in the following format:
        2023-02-21 16:30:07.465055
        2023-02-21 16:30:08.470
    so as naive dates. This is the only format that works with queries like:
        Tweet.select().where(Tweet.created_at.minute == 11)

    This class extends the std class DateTimeField by ensuring that it only deals
     with dates in UTC timezone.
    """

    def db_value(self, value):
        if not isinstance(value, datetime):
            raise NotADatetime
        if not value.tzinfo:
            raise NaiveDatetime
        # Convert the date to UTC timezone and then remove the timezone info. as it must
        #  be stored as naive datetime.
        value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return super().db_value(value)

    def python_value(self, value):
        dt = super().python_value(value)
        if not isinstance(dt, datetime):
            raise NotADatetime
        return dt.replace(tzinfo=timezone.utc)
