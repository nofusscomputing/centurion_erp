from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import ReadOnlyModelViewSetInheritedCases

from core.viewsets.history import ViewSet

from itam.models.device import Device



class HistoryViewsetList(
    ReadOnlyModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_v2_model_history'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        device = Device.objects.create(
            organization = self.organization,
            name = 'dev'
        )

        self.kwargs = {
            'app_label': device._meta.app_label,
            'model_name': device._meta.model_name,
            'model_id': device.id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)
