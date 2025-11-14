import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.model_ticketcategory
class TicketCategorySerializerTestCases(
    SerializerTestCases
):
    pass


class TicketCategorySerializerInheritedCases(
    TicketCategorySerializerTestCases
):
    pass


@pytest.mark.module_core
class TicketCategorySerializerPyTest(
    TicketCategorySerializerTestCases
):
    pass