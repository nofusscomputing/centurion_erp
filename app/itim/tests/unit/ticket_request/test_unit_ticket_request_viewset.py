from django.test import TestCase

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases,
)

from itim.models.request_ticket import RequestTicket



class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):

    model = RequestTicket


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        if self.model is None:

            self.model = RequestTicket

        super().setUpTestData()


class TicketRequestViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    pass


    
