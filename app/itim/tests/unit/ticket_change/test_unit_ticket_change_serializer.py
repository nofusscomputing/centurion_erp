import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_serializer import (
    TicketBaseSerializerInheritedCases
)



@pytest.mark.model_changeticket
class ChangeTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases
):
    pass



class ChangeTicketSerializerInheritedCases(
    ChangeTicketSerializerTestCases
):
    pass



@pytest.mark.module_itim
class ChangeTicketSerializerPyTest(
    ChangeTicketSerializerTestCases
):
    pass