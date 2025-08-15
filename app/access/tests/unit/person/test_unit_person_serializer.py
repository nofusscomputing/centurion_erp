import pytest

from access.tests.unit.entity.test_unit_entity_serializer import (
    EntitySerializerInheritedCases
)



@pytest.mark.model_person
class PersonSerializerTestCases(
    EntitySerializerInheritedCases
):
    pass



class PersonSerializerInheritedCases(
    PersonSerializerTestCases
):
    pass



@pytest.mark.module_access
class PersonSerializerPyTest(
    PersonSerializerTestCases
):
    pass