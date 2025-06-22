import pytest
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from api.tests.unit.test_unit_common_viewset import PublicReadOnlyViewSetInheritedCases

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.viewsets.public_feature_flag import ViewSet

from itam.models.software import Software


@pytest.mark.skip( reason = "Audit history requires context['user']")
class ViewsetList(
    PublicReadOnlyViewSetInheritedCases,
    TestCase,
):

    viewset = ViewSet

    route_name = 'v2:public:devops:_api_checkin'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. make list request
        """


        super().setUpTestData()

        software = Software.objects.create(
            organization = self.organization,
            name = 'software'
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True,
        )

        self.kwargs = {
            'organization_id': self.organization.id,
            'software_id': software.id,
        }


        client = Client()
        
        url = reverse(
            self.route_name + '-list',
            kwargs = self.kwargs
        )

        self.http_options_response_list = client.options(url)
