import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)


@pytest.mark.model_entity
class EntitySerializerTestCases(
    SerializerTestCases
):
    pass



class EntitySerializerInheritedCases(
    EntitySerializerTestCases
):
    pass



@pytest.mark.module_access
class EntitySerializerPyTest(
    EntitySerializerTestCases
):
    pass