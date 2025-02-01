from typing import get_type_hints


class IntrospectableDataclass:
    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_fields(cls):
        return cls.__dataclass_fields__

    @classmethod
    def get_annotations(cls):
        return get_type_hints(cls)  # Or: cls.__annotations__.


class BaseDataclass(IntrospectableDataclass):
    """
    Example:
        @dataclass
        class ExerciseFactory(dataclass_utils.BaseDataclass):
            name_it: str | None = None
            name_en: str | None = None
    """

    pass
