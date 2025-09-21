import pytest

from django.test import TestCase

from itim.models.request_ticket import RequestTicket
from itim.tests.functional.ticket_slm.test_functional_ticket_slm_metadata import SLMTicketMetadataInheritedCases



@pytest.mark.model_requestticket
class MetadataTestCases(
    SLMTicketMetadataInheritedCases,
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
    MetadataTestCases,
):

    model = None



@pytest.mark.module_itim
class RequestTicketTest(
    MetadataTestCases,
    TestCase,

):

    pass
