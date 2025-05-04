from django.test import TestCase

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases,
)

from itim.models.request_ticket import RequestTicket



class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):

    model = RequestTicket



class TicketRequestViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass


    
