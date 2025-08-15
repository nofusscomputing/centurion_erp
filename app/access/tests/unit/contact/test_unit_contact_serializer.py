import pytest

from access.tests.unit.person.test_unit_person_serializer import (
    PersonSerializerInheritedCases
)



@pytest.mark.model_contact
class ContactSerializerTestCases(
    PersonSerializerInheritedCases
):
    pass



class ContactSerializerInheritedCases(
    ContactSerializerTestCases
):
    pass



@pytest.mark.module_access
class ContactSerializerPyTest(
    ContactSerializerTestCases
):
    pass