import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_serializer import (
    TicketBaseSerializerInheritedCases
)



@pytest.mark.model_problemticket
class ProblemTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases
):
    pass



class ProblemTicketSerializerInheritedCases(
    ProblemTicketSerializerTestCases
):
    pass



@pytest.mark.module_itim
class ProblemTicketSerializerPyTest(
    ProblemTicketSerializerTestCases
):
    pass