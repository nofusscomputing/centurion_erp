import pytest

from itim.tests.unit.ticket_slm.test_unit_ticket_slm_serializer import (
    SLMTicketSerializerInheritedCases
)



@pytest.mark.model_incidentticket
class IncidentTicketSerializerTestCases(
    SLMTicketSerializerInheritedCases
):
    pass


class IncidentTicketSerializerInheritedCases(
    IncidentTicketSerializerTestCases
):
    pass



@pytest.mark.module_itim
class IncidentTicketSerializerPyTest(
    IncidentTicketSerializerTestCases
):
    pass