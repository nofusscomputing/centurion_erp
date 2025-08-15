import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_metadata import TicketBaseMetadataInheritedCases

from itim.models.slm_ticket_base import SLMTicket



@pytest.mark.model_slmticket
class MetadataTestCases(
    TicketBaseMetadataInheritedCases,
):


    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

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



class SLMTicketMetadataInheritedCases(
    MetadataTestCases,
):

    model = None



# class SLMTicketTest(
#     MetadataTestCases,
#     TestCase,

# ):

#     pass
