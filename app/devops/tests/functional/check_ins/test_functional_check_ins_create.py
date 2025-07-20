import pytest

from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.tenant import Tenant as Organization

from devops.models.feature_flag_history import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software

from devops.models.check_ins import CheckIn



class Checkin(
    TestCase,
):
    """Check In entry created test cases

    When a deployment checks in, a checkin entry must be created.
    """

    model = CheckIn


    @classmethod
    def setUpTestData(self):

        self.organization = Organization.objects.create(name='test_org')


        self.software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = self.software,
            enabled = True
        )

        self.obj = FeatureFlag.objects.create(
            organization = self.organization,
            name = 'a name',
            software = self.software,
            enabled = True,
        )

        self.client = Client()

        self.headers = {
            'client-id': 'abcd1234',
            'User-Agent': 'My Software 1.2.3'
        }


    def test_check_in_created_feature_flag(self):
        """ CheckIn entry must be made
        
        When checking for feature flags, a CheckIn entry must be created.
        """

        url = reverse(
            'v2:public:devops:_api_checkin-list',
            kwargs={
                'organization_id': self.organization.id,
                'software_id': self.software.id,
            }
        )

        response = self.client.get(url, headers = self.headers)

        assert response.status_code == 200    # Depends upon a successful request

        version = str(self.client.headers['User-Agent']).split(' ')
        version = version[( len(version) - 1 )]

        entry = self.model.objects.filter(
            feature = 'feature_flag',
            version = version,
            software = self.software,
            deployment_id = self.client.headers['client-id'],
        )

        assert len(entry) == 1


    def test_check_in_created_feature_flag_not_modified(self):
        """ CheckIn entry must be made
        
        When checking for feature flags, a CheckIn entry must be created.
        """

        url = reverse(
            'v2:public:devops:_api_checkin-list',
            kwargs={
                'organization_id': self.organization.id,
                'software_id': self.software.id,
            }
        )

        headers = self.headers.copy()

        headers['If-Modified-Since'] = self.obj.created.strftime('%a, %d %b %Y %H:%M:%S %z')

        response = self.client.get(url, headers = headers)

        assert response.status_code == 304    # Depends upon a successful request

        version = str(self.client.headers['User-Agent']).split(' ')
        version = version[( len(version) - 1 )]

        entry = self.model.objects.filter(
            feature = 'feature_flag',
            version = version,
            software = self.software,
            deployment_id = self.client.headers['client-id'],
        )

        assert len(entry) == 1
