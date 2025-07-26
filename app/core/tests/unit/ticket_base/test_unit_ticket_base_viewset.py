import pytest
from django.test import Client, TestCase

from rest_framework.reverse import reverse


from core.viewsets.ticket import (
    NoDocsViewSet,
    TicketBase,
    ViewSet,
)

from api.tests.unit.test_unit_common_viewset import SubModelViewSetInheritedCases



@pytest.mark.skip(reason = 'see #895, tests being refactored')
@pytest.mark.model_ticketbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):

    model = None

    viewset = ViewSet

    base_model = TicketBase

    route_name = None


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        if self.model is None:

            self.model = TicketBase

        super().setUpTestData()

        if self.model != TicketBase:

            self.kwargs = {
                'ticket_type': self.model._meta.sub_model_type
            }

            self.viewset.kwargs = self.kwargs



        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)



    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg == 'ticket_type'



class TicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketBase.
    """

    model: str = None
    """name of the model to test"""

    route_name = 'v2:_api_ticketbase_sub'


@pytest.mark.module_core
class TicketBaseViewsetTest(
    ViewsetTestCases,
    TestCase,
):

    route_name = 'v2:_api_ticketbase'

    viewset = NoDocsViewSet
