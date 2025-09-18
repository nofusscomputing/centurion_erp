import pytest

from itim.tests.unit.ticket_slm.test_unit_ticket_slm_serializer import (
    SLMTicketSerializerInheritedCases
)



@pytest.mark.model_requestticket
class RequestTicketSerializerTestCases(
    SLMTicketSerializerInheritedCases
):
    pass


class RequestTicketSerializerInheritedCases(
    RequestTicketSerializerTestCases
):
    pass



@pytest.mark.module_assistance
class RequestTicketSerializerPyTest(
    RequestTicketSerializerTestCases
):
    pass