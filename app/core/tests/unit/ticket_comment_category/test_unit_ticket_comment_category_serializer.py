import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.model_ticketcategory
class TicketCommentCategorySerializerTestCases(
    SerializerTestCases
):
    pass


class TicketCommentCategorySerializerInheritedCases(
    TicketCommentCategorySerializerTestCases
):
    pass


@pytest.mark.module_core
class TicketCommentCategorySerializerPyTest(
    TicketCommentCategorySerializerTestCases
):
    pass