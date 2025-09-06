from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelListRetrieveDeleteViewSetInheritedCases

from core.models.ticket.ticket import Ticket
from core.viewsets.related_ticket import ViewSet



@pytest.mark.skip(reason = 'see #895, tests being refactored')
class TicketCommentViewsetList(
    ModelListRetrieveDeleteViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_ticket_comment'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        ticket_one = Ticket.objects.create(
            organization = self.organization,
            title = 'tick title',
            description = 'desc',
            ticket_type = Ticket.TicketType.REQUEST,
            opened_by = self.view_user
        )

        self.kwargs = {
            'ticket_id': ticket_one.id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)
