import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)


@pytest.mark.model_knowledgebase
class KnowledgeBaseSerializerTestCases(
    SerializerTestCases
):
    pass



class KnowledgeBaseSerializerInheritedCases(
    KnowledgeBaseSerializerTestCases
):
    pass



@pytest.mark.module_module_assistance
class KnowledgeBaseSerializerPyTest(
    KnowledgeBaseSerializerTestCases
):
    pass