import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_serializer import (
    TicketBaseSerializerInheritedCases
)



@pytest.mark.model_slmticket
class SLMTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases
):
    pass



class SLMTicketSerializerInheritedCases(
    SLMTicketSerializerTestCases
):
    pass



@pytest.mark.module_itim
class SLMTicketSerializerPyTest(
    SLMTicketSerializerTestCases
):
    pass