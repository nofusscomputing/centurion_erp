from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ModelListRetrieveDeleteViewSetInheritedCases

from core.models.ticket.ticket import Ticket
from core.viewsets.related_ticket import ViewSet



class RelatedTicketViewsetList(
    ModelListRetrieveDeleteViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_ticket_related'


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
