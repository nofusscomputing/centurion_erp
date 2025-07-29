import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)


@pytest.mark.model_knowledgebasecategory
class knowledgebaseCategorySerializerTestCases(
    SerializerTestCases
):
    pass



class knowledgebaseCategorySerializerInheritedCases(
    knowledgebaseCategorySerializerTestCases
):
    pass



@pytest.mark.module_module_assistance
class knowledgebaseCategorySerializerPyTest(
    knowledgebaseCategorySerializerTestCases
):
    pass