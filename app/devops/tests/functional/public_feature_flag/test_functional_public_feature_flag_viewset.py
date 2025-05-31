import pytest
from datetime import datetime
from dateutil import tz

from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.tenant import Tenant as Organization

from api.tests.abstract.api_serializer_viewset import SerializerView

from devops.models.feature_flag import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



@pytest.mark.skip( reason = "Audit history requires context['user']")
class ViewSetBase:

    model = FeatureFlag

    app_namespace = 'v2'
    
    url_name = 'public:devops:_public_api_v2_feature_flag'


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization


        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two',
            software = software,
        )


        self.url_view_kwargs = {
            'organization_id': self.organization.id,
            'software_id': software.id,
        }

        self.software_not_enabled = Software.objects.create(
            organization = self.organization,
            name = 'soft not enabled',
        )



class PermissionsAPI(
    ViewSetBase,
    TestCase,
):


    def test_view_user_anon_has_permission(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



class ViewSet(
    ViewSetBase,
    SerializerView,
    TestCase
):


    def test_returned_serializer_user_view(self):
        """ Check correct Serializer is returned

        View action for view user must return `ViewSerializer`
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ViewSerializer')



    def test_view_cache_without_header_if_modified_since(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is not supplied the date is to
        be supplied to the client

        Status must be HTTP/200
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



    def test_view_cache_with_header_if_modified_since_changed(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client.

        Status must be HTTP/200
        """

        client = Client(
            headers = {
                'If-Modified-Since': datetime.fromtimestamp(
                    self.item.modified.timestamp() - 86400,
                    tz=tz.tzutc()
                    )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



    def test_view_cache_with_header_if_modified_since_no_changed_date_less(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client

        Status must be HTTP/304
        """

        client = Client(
            headers = {
                'If-Modified-Since': datetime.fromtimestamp(
                    self.item.modified.timestamp() + 3600,
                    tz=tz.tzutc()
                ).strftime(
                    '%a, %d %b %Y %H:%M:%S %z'
                )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 304



    def test_view_cache_with_header_if_modified_since_no_changed_date_same(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client

        Status must be HTTP/304
        """

        client = Client(
            headers = {
                'If-Modified-Since': self.item.modified.strftime(
                    '%a, %d %b %Y %H:%M:%S %z'
                )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 304



    def test_view_software_exists_feature_flagging_not_enabled_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        Even if the org exists, return not found so as to not leak that the org exists.
        Even if software exists, return not found so as to not leak if software exists

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['organization_id'] = self.different_organization.id

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404



    def test_view_software_not_exists_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        Just like when software exists, return not found so as not to allude to existance of software.

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['software_id'] = 99999

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404



    def test_view_organization_not_exists_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        just like if org exists, return not found so as not to allude to existance of organization.

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['organization_id'] = 99999

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404


