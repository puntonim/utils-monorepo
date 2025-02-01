# import json
# from typing import Optional

# import pydantic
# from gymiq.utils import text_utils
# from gymiq.utils.pydantic_utils import (
#     PeeweeModelForCamelCaseSchema,
#     SoftValidationSchema,
# )

# TODO more tests =)


class TestPeeweeModelForCamelCaseSchema:
    class ExerciseSchema(PeeweeModelForCamelCaseSchema):
        id: int
        name_en: str

    def test_dump_camel_case_json_output(self):
        """
        From a snake case (typical Python) input we should be able to serialize
         JSON output in camel case (typical JSON).
        This is what a typical ReadView would do reading from DB and producing JSON.
        """
        data = dict(id=1, name_en="push up")
        out = self.ExerciseSchema(**data).json(by_alias=True)
        # Ensure all output keys are in data, if converted to snake.
        for key in json.loads(out):
            assert text_utils.camel_to_snake(key) in data
        # Ensure the output is exactly what we expect (a bit redundant).
        assert out == json.dumps(dict(id=1, nameEn="push up"))

    def test_dump_snake_case_json_output(self):
        """
        From a snake case (typical Python) input we should be able to serialize
         JSON output in the same snake case.
        This is just the default behavior that should not be broken.
        """
        data = dict(id=1, name_en="push up")
        out = self.ExerciseSchema(**data).json()  # default: `by_alias=False`.
        # Ensure all output keys converted to snake are in data.
        for key in json.loads(out):
            assert key in data
        # Ensure the output is exactly what we expect (a bit redundant).
        assert out == json.dumps(data)

    def test_load_camel_case_dict_input(self):
        """
        From a camel case (typical JSON) input we should be able to load a regular
         Python object with snake case (typical Python) attrs.
        This is what a typical CreateView would do reading from JSON POST input and
         instantiating a Python object (that eventually might turn into a DB model).
        """
        data = dict(id=1, nameEn="push up")
        exercise = self.ExerciseSchema(**data)
        # Ensure exercise has snake attrs.
        assert exercise.name_en == data["nameEn"]
        # Ensure the dict version of exercise is exactly what we expect (a bit redundant).
        assert exercise.to_dict() == dict(id=1, name_en="push up")


class TestSoftValidationSchema:
    class QueryStringSchema(SoftValidationSchema):
        id: Optional[int] = pydantic.Field(default=None)
        name_en: Optional[str]

    def test_happy_flow(self):
        schema = self.QueryStringSchema(id=2, name_en="push up")
        assert schema.id == 2
        assert schema.name_en == "push up"

        schema = self.QueryStringSchema(
            id="XXX",
            name_en=Optional,  # Optional is just a random non-serializable thing.
        )
        assert schema.id is None
        assert schema.name_en is None
