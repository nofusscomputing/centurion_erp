import django
import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import SubModelViewSetInheritedCases

from core.viewsets.ticket_comment import (
    NoDocsViewSet,
    TicketBase,
    TicketCommentBase,
    ViewSet
)

User = django.contrib.auth.get_user_model()



@pytest.mark.model_ticketcommentbase
class TicketCommentBaseViewsetTestCases(
    SubModelViewSetInheritedCases,
):

    model = None

    viewset = ViewSet

    base_model = TicketCommentBase

    route_name = None


    @classmethod
    def setUpTestData(self):


        self.viewset = ViewSet


        if self.model is None:

            self.model = TicketCommentBase



        super().setUpTestData()

        self.ticket = TicketBase.objects.create(
            organization = self.organization,
            title = 'ticket comment test',
            opened_by = self.view_user,
        )

        self.kwargs = {
            'ticket_id': self.ticket.id
        }

        if self.model is not TicketCommentBase:

            self.kwargs = {
                **self.kwargs,
                'ticket_comment_model': self.model._meta.sub_model_type
            }

        self.viewset.kwargs = self.kwargs


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)


    @classmethod
    def tearDownClass(cls):

        cls.ticket.delete()

        super().tearDownClass()



    def test_view_attr_value_model_kwarg(self):
        """Attribute Test

        Attribute `model_kwarg` must be equal to model._meta.sub_model_type
        """

        view_set = self.viewset()

        assert view_set.model_kwarg == 'ticket_comment_model'



class TicketCommentBaseViewsetInheritedCases(
    TicketCommentBaseViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketCommentBase
    
    Use this Test suit if your sub-model inherits directly from TicketCommentBase.
    """

    model: str = None
    """name of the model to test"""

    route_name = 'v2:_api_ticket_comment_base_sub'



@pytest.mark.module_core
class TicketCommentBaseViewsetTest(
    TicketCommentBaseViewsetTestCases,
    TestCase,
):

    kwargs = {}

    route_name = 'v2:_api_ticket_comment_base'

    viewset = NoDocsViewSet
