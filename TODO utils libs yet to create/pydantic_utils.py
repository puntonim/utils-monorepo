from typing import Any, Optional, Sequence, get_type_hints

import peewee
import pydantic
from pydantic.utils import GetterDict

from . import text_utils


class _IntrospectablePydanticSchema:
    """
    Inherit this mixin in the base class used by any Pydantic schema in this codebase
     in order to provide some useful introspection methods.
    """

    _FORCE_NON_REQUIRED = set()
    _FORCE_REQUIRED = set()

    def to_dict(self, *args, **kwargs):
        return self.dict(*args, **kwargs)

    @classmethod
    def get_fields(cls):
        return cls.__fields__

    @classmethod
    def get_required_field_names(cls) -> set:
        required = set(x.name for x in cls.get_fields().values() if x.required)
        return required.union(cls._FORCE_REQUIRED) - cls._FORCE_NON_REQUIRED

    @classmethod
    def get_non_required_field_names(cls) -> set:
        non_required = set(x.name for x in cls.get_fields().values() if not x.required)
        return non_required.union(cls._FORCE_NON_REQUIRED) - cls._FORCE_REQUIRED

    @classmethod
    def get_annotations(cls):
        return get_type_hints(cls)  # Or: cls.__annotations__.


class BasePydanticSchema(pydantic.BaseModel, _IntrospectablePydanticSchema):
    """
    Use this as a base class for any Pydantic schema in this codebase.
    """

    pass


class BasePeeweeModelSchema(BasePydanticSchema):
    """
    Use this as a base class for any schema that is initialized with a PeeWee
     model instance.

    Example:
        class ExerciseSchema(BasePeeweeModelSchema):
            id: int
            name_en: str
            muscles_en: list[str]

        exercise = Exercise.get_by_id(1)  # Read from DB.
        schema = ExerciseSchema.from_orm(exercise)
        assert schema.id == exercise.id
        assert schema.name_en == exercise.name_en
        assert schema.muscles_en == exercise.muscles_en
    """

    class Config:
        class PeeweeModelGetterDict(GetterDict):
            def get(self, key: Any, default: Any = None):
                if hasattr(self._obj, key):
                    return super().get(key, default)
                res = getattr(self._obj, text_utils.camel_to_snake(key), default)
                return res

        orm_mode = True
        getter_dict = PeeweeModelGetterDict


class PeeweeModelForCamelCaseSchema(BasePeeweeModelSchema):
    """
    Inherit this mixin when serializing to JSON camelCase output
     or loading from dict camelCase input.

    Example:
        class ExerciseSchema(PeeweeModelForCamelCaseSchema):
            id: int
            name_en: str

        # Serialize PeeWee model instance to JSON camelCase:
        exercise = Exercise.get_by_id(1)  # Read from DB.
        schema = ExerciseSchema.from_orm(exercise)
        schema.json(by_alias=True)
        >>> "{'id': 1, 'nameEn': 'push up'}"

        # Load camelCase dict:
        data = dict(id=1, nameEn="push up")
        schema = ExerciseSchema(**data)
        schema.name_en
        >>> "push up"
    """

    class Config:
        # Generate the camelCase alias for each field.
        alias_generator = text_utils.snake_to_camel
        # Allow the population of fields by both their names or aliases.
        allow_population_by_field_name = True


class PeeweeModelForeignKeysAsIdsSchema(BasePeeweeModelSchema):
    """
    Inherit this mixin when serializing to JSON fields that are PeeWee models.
     The typical use case is for Foreign Keys. The output is model.id.

    Example:
        class ExerciseSchema(PeeweeModelForeignKeysAsIdsSchema):
            id: int
            name_en: str
            superset: Optional[Exercise]  # ForeignKey to Exercise (itself).

        # Serialize to JSON:
        exercise = Exercise.get_by_id(2)  # Read from DB.
        schema = ExerciseSchema.from_orm(exercise)
        schema.json()
        >>> "{'id': 1, 'nameEn': 'push up', 'superset': 33}"
    """

    class Config:
        # TODO could we return the relative url (e.g. exercise/{id}) instead of just
        #  the id? If so, it should be in a new field, so we would have
        #  2 fields like: supersetId and supersetUri.
        json_encoders = {
            peewee.Model: lambda model: model.id,
            peewee.ManyToManyQuery: lambda q: [model.id for model in q],
        }
        arbitrary_types_allowed = True


class SoftValidationSchema(BasePydanticSchema):
    """
    Inherit this mixin when the Pydantic schema should not raise any ValidationError
     but instead set the value to the default or None, in case of validation error.
    Typical use case: parsing URL query string.

    Example:
        class QueryStringSchema(SoftValidationSchema):
            id: Optional[int] = pydantic.Field(default=None)
            name_en: Optional[str]

        schema = QueryStringSchema(
            id="XXX",
            name_en=Optional,  # Optional is just a random non-serializable thing.
        )
        assert schema.id is None
        assert schema.name_en is None
    """

    @pydantic.validator("*", pre=True)
    def validate_any_field(cls, value, values, config, field):
        """
        Validate any field without raising any exception but instead setting its
         value to the default, in case of validation error.
        """
        # We need to use a hack to avoid infinite recursion.
        # Storing the var `__has_validation_run_already` in `values` is the safest way
        #  as we cannot change the signature of this method, and also we cannot mess up
        #  with class vars as `config` (mind that this is a class method).
        has_validation_run_already = values.get("__has_validation_run_already")
        if not has_validation_run_already:
            values["__has_validation_run_already"] = True
            # Call the original validator for this field (but avoiding the recursion
            #  with the hack).
            value, error = field.validate(value, values, loc=field.alias, cls=cls)
            del values["__has_validation_run_already"]
            if error:
                # Do not raise the exc, but just set the value to the default or None.
                value = field.default
        return value


class AllFieldsOptionalSchema(BasePydanticSchema):
    """
    Inherit this mixin when all fields in the pydantic schema should be optional,
     despite their actual definition.

    Example:
        class ExerciseUpdateSchema(AllFieldsOptionalSchema):
            id: int
            name_en: str

        schema = ExerciseUpdateSchema(name_en="foo")
        assert schema
    """

    def __new__(cls, *args, **kwargs):
        # Set all fields as optional.
        instance = super().__new__(cls)
        for field in instance.get_fields().values():
            field.required = False
        return instance


def create_schema_from_peewee_model(
    peewee_model, base_pydantic_schema=BasePydanticSchema
):
    """
    Given a Peewee model properly annotated with type annotations, it returns the
     matching Pydantic schema named after the model.

    *Make sure peewee_model is properly annotated!*

    Provide the `base_pydantic_schema` arg to force those attrs:
     - with a ForeignKey or
     - with default values.
     See complex example underneath.

    Example, simple:
        class Muscle(peewee_utils.BasePeeweeModel):
            id: int = peewee.AutoField()
            name_it: str = peewee.CharField(max_length=75, unique=True)

        MuscleSchema = pydantic_utils.create_schema_from_peewee_model(Muscle)
        >>> MuscleSchema.__fields__
        >>> {'id': ModelField(name='id', type=int, required=True),
             'name_it': ModelField(name='name_it', type=str, required=True)}

    Example, complex:
        class Exercise(peewee_utils.BasePeeweeModel):
            id: int = peewee.AutoField()
            created_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
            name_it: str = peewee.CharField(max_length=128, unique=True)
            body_sections_it: list[str] = JSONField()
            is_superset: bool = peewee.BooleanField(default=False)
            superset: Optional["Exercise"] = peewee.ForeignKeyField("self", backref="single_exercises", on_delete="RESTRICT", null=True)

        class _BaseExerciseSchema(BasePydanticSchema):
            superset: Optional[Exercise] = None
            is_superset: bool = False

            class Config:
                arbitrary_types_allowed = True

        ExerciseSchema = pydantic_utils.create_schema_from_peewee_model(Exercise, _BaseExerciseSchema)
        >>> ExerciseSchema.__fields__
        >>> {'id': ModelField(name='id', type=int, required=True),
             'created_at': ModelField(name='created_at', type=datetime, required=True),
             'name_it': ModelField(name='name_it', type=str, required=True),
             'body_sections_it': ModelField(name='body_sections_it', type=List[str], required=True),
             'is_superset': ModelField(name='is_superset', type=bool, required=False, default=False),
             'superset': ModelField(name='superset', type=Optional[Exercise], required=False, default=None)}
    """
    kwargs = dict()
    for attr_name, annotation in peewee_model.get_annotations().items():
        default = ...
        if "Optional" in str(annotation):
            default = None
        if base_pydantic_schema and attr_name in base_pydantic_schema.__fields__.keys():
            continue
        kwargs[attr_name] = (annotation, default)
    return pydantic.create_model(
        peewee_model.__name__ + "Schema", **kwargs, __base__=base_pydantic_schema
    )


def do_not_inherit_fields_from_pydantic_parent_class(
    field_names: Optional[Sequence] = None,
):
    """
    Decorator to be used on a class definition when using inheritance but some
     fields in the parent class need NOT be inherited.

    Example:
        class ExerciseSchema(BasePydanticSchema):
            id: int
            name: str

        do_not_inherit_fields_from_pydantic_parent_class(["id"])
        class ExerciseDomain(ExerciseSchema):
            pass

        The effect is that the class ExerciseDomain does not have the field `id`.
    """
    if field_names is None:
        field_names = tuple()

    def wrapper(cls):  # `cls` is the decorated class.
        for field_name in field_names:
            try:
                del cls.__fields__[field_name]
            except AttributeError:
                pass
        return cls

    return wrapper
