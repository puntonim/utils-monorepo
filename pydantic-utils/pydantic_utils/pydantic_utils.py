from typing import Any, Type, TypeVar

import pydantic
from pydantic import (
    BaseModel,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    create_model,
)
from pydantic.fields import FieldInfo
from pydantic.functional_validators import WrapValidator
from pydantic_core import PydanticUseDefault


class _IntrospectablePydanticSchemaMixin:
    """
    Inherit this mixin in a pydantic.BaseModel class and use it in any Pydantic schema
     in order to provide some useful introspection methods.
    """

    _FORCE_NON_REQUIRED = set()
    _FORCE_REQUIRED = set()

    def to_dict(self, *args, **kwargs):
        return self.dict(*args, **kwargs)

    @classmethod
    def get_fields(cls) -> dict[str, FieldInfo]:
        return cls.model_fields

    @classmethod
    def get_required_field_names(cls) -> set[str]:
        required = set(
            name for name, info in cls.get_fields().items() if info.is_required()
        )
        return required.union(cls._FORCE_REQUIRED) - cls._FORCE_NON_REQUIRED

    @classmethod
    def get_non_required_field_names(cls) -> set[str]:
        non_required = set(
            name for name, info in cls.get_fields().items() if not info.is_required()
        )
        return non_required.union(cls._FORCE_NON_REQUIRED) - cls._FORCE_REQUIRED

    @classmethod
    def get_annotations(cls) -> dict[str, Type]:
        return {name: info.annotation for name, info in cls.get_fields().items()}


## Older version for Pydantic 1.*
# class _IntrospectablePydanticSchema:
#     """
#     Inherit this mixin in the base class used by any Pydantic schema in order to
#      provide some useful introspection methods.
#     """
#
#     _FORCE_NON_REQUIRED = set()
#     _FORCE_REQUIRED = set()
#
#     def to_dict(self, *args, **kwargs):
#         return self.dict(*args, **kwargs)
#
#     @classmethod
#     def get_fields(cls):
#         return cls.__fields__
#
#     @classmethod
#     def get_required_field_names(cls) -> set:
#         required = set(x.name for x in cls.get_fields().values() if x.required)
#         return required.union(cls._FORCE_REQUIRED) - cls._FORCE_NON_REQUIRED
#
#     @classmethod
#     def get_non_required_field_names(cls) -> set:
#         non_required = set(x.name for x in cls.get_fields().values() if not x.required)
#         return non_required.union(cls._FORCE_NON_REQUIRED) - cls._FORCE_REQUIRED
#
#     @classmethod
#     def get_annotations(cls):
#         return get_type_hints(cls)  # Or: cls.__annotations__.


class BasePydanticSchema(pydantic.BaseModel, _IntrospectablePydanticSchemaMixin):
    """
    Use this as a base class for any Pydantic schema in this codebase.
    """

    pass


# Src: https://github.com/pydantic/pydantic/discussions/7867
def UseDefaultWhenValidationError() -> WrapValidator:
    """
    Use this function in a Field definition to make it return the default value
     instead of raising a validation error.
    Typical use case: Fields when parsing URL query string.

    Example:
        from typing import Annotated
        class QueryStringSchema(pydantic_utils.BasePydanticSchema):
            id: int | None = None
            name_en: (
                Annotated[int, pydantic_utils.UseDefaultWhenValidationError()] | None
            ) = None

        schema = self.QueryStringSchema(
            id=123, name_en=IOError  # IOError is just a random non-serializable thing.
        )
        assert schema.id == 123
        assert schema.name_en is None
    """

    def _inner(
        value: Any,
        handler: ValidatorFunctionWrapHandler,
        _info: ValidationInfo,
    ) -> Any:
        try:
            return handler(value)
        except pydantic.ValidationError as error:
            raise PydanticUseDefault from error

    return WrapValidator(_inner)


B = TypeVar("B", bound=BaseModel)


def model_use_default_when_validation_error(model_cls: type[B]) -> type[B]:
    """
    Use this decorator in a Model definition to make all its fields return default
     values instead of raising validation errors.
    Typical use case: Fields when parsing URL query string.

    Example:
        @pydantic_utils.model_use_default_when_validation_error
        class QueryStringSchema(pydantic_utils.BasePydanticSchema):
            id: int | None = None
            name_en: int | None = None

        schema = self.QueryStringSchema(
            id="XXX",
            name_en=IOError,  # IOError is just a random non-serializable thing.
        )
        assert schema.id is None
        assert schema.name_en is None
    """

    for field_info in model_cls.model_fields.values():
        if (
            not field_info.is_required()
        ):  # Only add this validator if a default is present, throws errors otherwise
            field_info.metadata.append(UseDefaultWhenValidationError())

    return create_model(
        model_cls.__name__,
        __base__=model_cls,
    )


## It does not work anymore in Pydantic 2.*.
# class AllFieldsOptionalSchemaMixin(BasePydanticSchema):
#     """
#     Inherit this mixin when all fields in the pydantic schema should be optional,
#      despite their actual definition.
#
#     Example:
#         class ExerciseUpdateSchema(AllFieldsOptionalSchema):
#             id: int
#             name_en: str
#
#         schema = ExerciseUpdateSchema(name_en="foo")
#         assert schema
#     """
#
#     def __new__(cls, *args, **kwargs):
#         # Set all fields as optional.
#         instance = super().__new__(cls)
#         for field in instance.get_fields().values():
#             field.required = False
#         return instance


## It does not work anymore in Pydantic 2.*.
# def do_not_inherit_fields_from_pydantic_parent_class(
#     field_names: Sequence | None = None,
# ):
#     """
#     Decorator to be used on a class definition when using inheritance but some
#      fields in the parent class need NOT be inherited.
#
#     Example:
#         class ExerciseSchema(BasePydanticSchema):
#             id: int
#             name: str
#
#         @do_not_inherit_fields_from_pydantic_parent_class(["id"])
#         class ExerciseDomain(ExerciseSchema):
#             pass
#
#         The effect is that the class ExerciseDomain does not have the field `id`.
#     """
#     if field_names is None:
#         field_names = tuple()
#
#     def wrapper(cls):  # `cls` is the decorated class.
#         for field_name in field_names:
#             try:
#                 del cls.__fields__[field_name]
#             except AttributeError:
#                 pass
#         return cls
#
#     return wrapper


########################################################################################
## The following Peewee classes for Pydantic were part of gymiq project.

# class BasePeeweeModelSchema(BasePydanticSchema):
#     """
#     Use this as a base class for any schema that is initialized with a PeeWee
#      model instance.
#
#     Example:
#         class ExerciseSchema(BasePeeweeModelSchema):
#             id: int
#             name_en: str
#             muscles_en: list[str]
#
#         exercise = Exercise.get_by_id(1)  # Read from DB.
#         schema = ExerciseSchema.from_orm(exercise)
#         assert schema.id == exercise.id
#         assert schema.name_en == exercise.name_en
#         assert schema.muscles_en == exercise.muscles_en
#     """
#
#     class Config:
#         class PeeweeModelGetterDict(GetterDict):
#             def get(self, key: Any, default: Any = None):
#                 if hasattr(self._obj, key):
#                     return super().get(key, default)
#                 res = getattr(self._obj, text_utils.camel_to_snake(key), default)
#                 return res
#
#         orm_mode = True
#         getter_dict = PeeweeModelGetterDict


# class PeeweeModelForCamelCaseSchema(BasePeeweeModelSchema):
#     """
#     Inherit this mixin when serializing to JSON camelCase output
#      or loading from dict camelCase input.
#
#     Example:
#         class ExerciseSchema(PeeweeModelForCamelCaseSchema):
#             id: int
#             name_en: str
#
#         # Serialize PeeWee model instance to JSON camelCase:
#         exercise = Exercise.get_by_id(1)  # Read from DB.
#         schema = ExerciseSchema.from_orm(exercise)
#         schema.json(by_alias=True)
#         >>> "{'id': 1, 'nameEn': 'push up'}"
#
#         # Load camelCase dict:
#         data = dict(id=1, nameEn="push up")
#         schema = ExerciseSchema(**data)
#         schema.name_en
#         >>> "push up"
#     """
#
#     class Config:
#         # Generate the camelCase alias for each field.
#         alias_generator = text_utils.snake_to_camel
#         # Allow the population of fields by both their names or aliases.
#         allow_population_by_field_name = True


# class PeeweeModelForeignKeysAsIdsSchema(BasePeeweeModelSchema):
#     """
#     Inherit this mixin when serializing to JSON fields that are PeeWee models.
#      The typical use case is for Foreign Keys. The output is model.id.
#
#     Example:
#         class ExerciseSchema(PeeweeModelForeignKeysAsIdsSchema):
#             id: int
#             name_en: str
#             superset: Optional[Exercise]  # ForeignKey to Exercise (itself).
#
#         # Serialize to JSON:
#         exercise = Exercise.get_by_id(2)  # Read from DB.
#         schema = ExerciseSchema.from_orm(exercise)
#         schema.json()
#         >>> "{'id': 1, 'nameEn': 'push up', 'superset': 33}"
#     """
#
#     class Config:
#         # TODO could we return the relative url (e.g. exercise/{id}) instead of just
#         #  the id? If so, it should be in a new field, so we would have
#         #  2 fields like: supersetId and supersetUri.
#         json_encoders = {
#             peewee.Model: lambda model: model.id,
#             peewee.ManyToManyQuery: lambda q: [model.id for model in q],
#         }
#         arbitrary_types_allowed = True


# def create_schema_from_peewee_model(
#     peewee_model, base_pydantic_schema=BasePydanticSchema
# ):
#     """
#     Given a Peewee model properly annotated with type annotations, it returns the
#      matching Pydantic schema named after the model.
#
#     *Make sure peewee_model is properly annotated!*
#
#     Provide the `base_pydantic_schema` arg to force those attrs:
#      - with a ForeignKey or
#      - with default values.
#      See complex example underneath.
#
#     Example, simple:
#         class Muscle(peewee_utils.BasePeeweeModel):
#             id: int = peewee.AutoField()
#             name_it: str = peewee.CharField(max_length=75, unique=True)
#
#         MuscleSchema = pydantic_utils.create_schema_from_peewee_model(Muscle)
#         >>> MuscleSchema.__fields__
#         >>> {'id': ModelField(name='id', type=int, required=True),
#              'name_it': ModelField(name='name_it', type=str, required=True)}
#
#     Example, complex:
#         class Exercise(peewee_utils.BasePeeweeModel):
#             id: int = peewee.AutoField()
#             created_at: datetime = peewee_utils.UtcDateTimeField(default=datetime_utils.now_utc)
#             name_it: str = peewee.CharField(max_length=128, unique=True)
#             body_sections_it: list[str] = JSONField()
#             is_superset: bool = peewee.BooleanField(default=False)
#             superset: Optional["Exercise"] = peewee.ForeignKeyField("self", backref="single_exercises", on_delete="RESTRICT", null=True)
#
#         class _BaseExerciseSchema(BasePydanticSchema):
#             superset: Optional[Exercise] = None
#             is_superset: bool = False
#
#             class Config:
#                 arbitrary_types_allowed = True
#
#         ExerciseSchema = pydantic_utils.create_schema_from_peewee_model(Exercise, _BaseExerciseSchema)
#         >>> ExerciseSchema.__fields__
#         >>> {'id': ModelField(name='id', type=int, required=True),
#              'created_at': ModelField(name='created_at', type=datetime, required=True),
#              'name_it': ModelField(name='name_it', type=str, required=True),
#              'body_sections_it': ModelField(name='body_sections_it', type=List[str], required=True),
#              'is_superset': ModelField(name='is_superset', type=bool, required=False, default=False),
#              'superset': ModelField(name='superset', type=Optional[Exercise], required=False, default=None)}
#     """
#     kwargs = dict()
#     for attr_name, annotation in peewee_model.get_annotations().items():
#         default = ...
#         if "Optional" in str(annotation):
#             default = None
#         if base_pydantic_schema and attr_name in base_pydantic_schema.__fields__.keys():
#             continue
#         kwargs[attr_name] = (annotation, default)
#     return pydantic.create_model(
#         peewee_model.__name__ + "Schema", **kwargs, __base__=base_pydantic_schema
#     )
