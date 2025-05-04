from django.test import TestCase

# from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import TicketBaseViewSetInheritedCases

from itim.models.request_ticket import RequestTicket
from itim.tests.functional.ticket_slm.test_functional_ticket_slm_viewset import SLMTicketViewSetInheritedCases


class ViewSetTestCases(
    SLMTicketViewSetInheritedCases,
):

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = RequestTicket


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            **self.kwargs_create_item_diff_org
        }

        super().setUpTestData()



class RequestTicketInheritedCases(
    ViewSetTestCases,
):

    model = None



class RequestTicketTest(
    ViewSetTestCases,
    TestCase,
):

    pass
