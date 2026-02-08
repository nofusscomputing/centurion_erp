import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.tickets
@pytest.mark.model_ticketdependency
class TicketDependencySerializerTestCases(
    SerializerTestCases
):
    pass


class TicketDependencySerializerInheritedCases(
    TicketDependencySerializerTestCases
):
    pass


@pytest.mark.module_core
class TicketDependencySerializerPyTest(
    TicketDependencySerializerTestCases
):
    pass