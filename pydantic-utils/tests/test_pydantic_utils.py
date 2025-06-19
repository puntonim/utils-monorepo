from typing import Annotated, Literal

import pydantic
from pydantic.fields import FieldInfo

import pydantic_utils
from pydantic_utils.pydantic_utils import _IntrospectablePydanticSchemaMixin


class TestIntrospectablePydanticSchema:
    class CarSchema(pydantic.BaseModel, _IntrospectablePydanticSchemaMixin):
        color: str
        n_wheels: int | None = None
        brand: Literal["Ferrari", "Fiat"]
        photo_url: pydantic.AnyHttpUrl | None = None

    def setup_method(self):
        self.schema = self.CarSchema(color="red", brand="Ferrari")

    def test_to_dict(self):
        assert self.schema.to_dict() == {
            "color": "red",
            "n_wheels": None,
            "brand": "Ferrari",
            "photo_url": None,
        }

    def test_get_fields(self):
        fields = self.schema.get_fields()
        assert isinstance(fields["color"], FieldInfo)
        assert isinstance(fields["n_wheels"], FieldInfo)
        assert isinstance(fields["brand"], FieldInfo)
        assert isinstance(fields["photo_url"], FieldInfo)

    def test_get_required_field_names(self):
        assert self.schema.get_required_field_names() == set(("color", "brand"))

    def test_get_non_required_field_names(self):
        assert self.schema.get_non_required_field_names() == {"n_wheels", "photo_url"}

    def test_get_annotations(self):
        annotations = self.schema.get_annotations()
        assert annotations["color"] == str
        assert annotations["n_wheels"] == int | None
        assert annotations["brand"] == Literal["Ferrari", "Fiat"]
        assert annotations["photo_url"] == pydantic.AnyHttpUrl | None


class TestUseDefaultWhenValidationError:
    class QueryStringSchema(pydantic_utils.BasePydanticSchema):
        id: int | None = None
        name_en: (
            Annotated[int, pydantic_utils.UseDefaultWhenValidationError()] | None
        ) = None

    def test_happy_flow(self):
        schema = self.QueryStringSchema(
            id=123, name_en=IOError  # IOError is just a random non-serializable thing.
        )
        assert schema.id == 123
        assert schema.name_en is None


class TestModelUseDefaultWhenValidationError:
    @pydantic_utils.model_use_default_when_validation_error
    class QueryStringSchema(pydantic_utils.BasePydanticSchema):
        id: int | None = None
        name_en: int | None = None

    def test_happy_flow(self):
        schema = self.QueryStringSchema(
            id="XXX",
            name_en=IOError,  # IOError is just a random non-serializable thing.
        )
        assert schema.id is None
        assert schema.name_en is None


# class TestPeeweeModelForCamelCaseSchema:
#     class ExerciseSchema(PeeweeModelForCamelCaseSchema):
#         id: int
#         name_en: str
#
#     def test_dump_camel_case_json_output(self):
#         """
#         From a snake case (typical Python) input we should be able to serialize
#          JSON output in camel case (typical JSON).
#         This is what a typical ReadView would do reading from DB and producing JSON.
#         """
#         data = dict(id=1, name_en="push up")
#         out = self.ExerciseSchema(**data).json(by_alias=True)
#         # Ensure all output keys are in data, if converted to snake.
#         for key in json.loads(out):
#             assert text_utils.camel_to_snake(key) in data
#         # Ensure the output is exactly what we expect (a bit redundant).
#         assert out == json.dumps(dict(id=1, nameEn="push up"))
#
#     def test_dump_snake_case_json_output(self):
#         """
#         From a snake case (typical Python) input we should be able to serialize
#          JSON output in the same snake case.
#         This is just the default behavior that should not be broken.
#         """
#         data = dict(id=1, name_en="push up")
#         out = self.ExerciseSchema(**data).json()  # default: `by_alias=False`.
#         # Ensure all output keys converted to snake are in data.
#         for key in json.loads(out):
#             assert key in data
#         # Ensure the output is exactly what we expect (a bit redundant).
#         assert out == json.dumps(data)
#
#     def test_load_camel_case_dict_input(self):
#         """
#         From a camel case (typical JSON) input we should be able to load a regular
#          Python object with snake case (typical Python) attrs.
#         This is what a typical CreateView would do reading from JSON POST input and
#          instantiating a Python object (that eventually might turn into a DB model).
#         """
#         data = dict(id=1, nameEn="push up")
#         exercise = self.ExerciseSchema(**data)
#         # Ensure exercise has snake attrs.
#         assert exercise.name_en == data["nameEn"]
#         # Ensure the dict version of exercise is exactly what we expect (a bit redundant).
#         assert exercise.to_dict() == dict(id=1, name_en="push up")
