import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from itam.models.device import Device
from itam.viewsets.device_operating_system import ViewSet



@pytest.mark.skip(reason = 'see #895, tests being refactored')
@pytest.mark.model_deviceoperatingsystem
@pytest.mark.module_itam
class DeviceOperatingSystemViewsetList(
    ModelViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:_api_deviceoperatingsystem'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        self.kwargs = {
            'device_id': Device.objects.create(
                organization = self.organization,
                name = 'dev'
            ).id
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        client.force_login(self.view_user)

        self.http_options_response_list = client.options(url)
