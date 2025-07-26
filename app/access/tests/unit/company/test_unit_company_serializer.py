import pytest

from access.tests.unit.entity.test_unit_entity_serializer import (
    EntitySerializerInheritedCases
)



@pytest.mark.model_company
class CompanySerializerTestCases(
    EntitySerializerInheritedCases
):
    pass



class CompanySerializerInheritedCases(
    CompanySerializerTestCases
):
    pass



@pytest.mark.module_access
class CompanySerializerPyTest(
    CompanySerializerTestCases
):
    pass