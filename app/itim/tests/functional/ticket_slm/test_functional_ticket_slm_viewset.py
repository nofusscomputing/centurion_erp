import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import TicketBaseViewSetInheritedCases

from itim.models.slm_ticket_base import SLMTicket




@pytest.mark.model_slmticket
class ViewSetTestCases(
    TicketBaseViewSetInheritedCases,
):

    kwargs_create_item = {}

    kwargs_create_item_diff_org = {}

    model = SLMTicket


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            'tto': 1,
            'ttr': 2,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            'tto': 1,
            'ttr': 2,
            **self.kwargs_create_item_diff_org
        }

        super().setUpTestData()



class SLMTicketViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None

    # kwargs_create_item: dict = None

    # kwargs_create_item_diff_org: dict = None



# class SLMTicketTest(
#     ViewSetTestCases,
#     TestCase,
# ):

#     pass
