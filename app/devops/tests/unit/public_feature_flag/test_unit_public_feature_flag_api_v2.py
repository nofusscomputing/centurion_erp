import pytest
from datetime import datetime

from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models.tenant import Tenant as Organization

from devops.models.feature_flag import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software


@pytest.mark.skip( reason = "Audit history requires context['user']")
class API(
    TestCase,
):

    model = FeatureFlag

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = self.software,
            enabled = True,
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            software = self.software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )

        self.url_view_kwargs = {
            'organization_id': self.organization.id,
            'software_id': self.software.id
        }

        self.id = str(self.item.created.year) + '-' + str(f'{self.item.id:05}')

        client = Client()
        url = reverse('v2:public:devops:_public_api_v2_feature_flag-list', kwargs=self.url_view_kwargs)


        self.response = client.get(url)

        self.api_data = self.response.data



    def test_api_header_exists_last_modified(self):
        """ Test for existance of HTTP Header

        Last-Modified header must exist
        """

        assert 'Last-Modified' in self.response.headers



    def test_api_header_type_last_modified(self):
        """ Test for type of HTTP Header

        Last-Modified header must be of type str
        """

        assert type(self.response.headers['Last-Modified']) is str



    def test_api_header_format_last_modified(self):
        """ Test the format of HTTP Header

        Convert to datetime. if converts without error and type is datetime
        it'll be considered in the correct format.

        Last-Modified Header Must be correct format.
        """

        converted = datetime.strptime(self.response.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %z')

        assert type(converted) is datetime



    def test_api_field_type_id(self):
        """ Test for type for API Field

        id field must be dict
        """

        assert type(self.api_data['results'][0][self.id]) is dict



    def test_api_field_exists_id_name(self):
        """ Test for existance of API Field

        id.name key must exist
        """

        assert 'name' in self.api_data['results'][0][self.id]


    def test_api_field_type_id_name(self):
        """ Test for type for API Field

        id.name field must be str
        """

        assert type(self.api_data['results'][0][self.id]['name']) is str



    def test_api_field_exists_id_description(self):
        """ Test for existance of API Field

        id.description key must exist
        """

        assert 'description' in self.api_data['results'][0][self.id]


    def test_api_field_type_id_description(self):
        """ Test for type for API Field

        id.description field must be str
        """

        assert type(self.api_data['results'][0][self.id]['description']) is str



    def test_api_field_exists_id_enabled(self):
        """ Test for existance of API Field

        id.enabled key must exist
        """

        assert 'enabled' in self.api_data['results'][0][self.id]


    def test_api_field_type_id_enabled(self):
        """ Test for type for API Field

        id.enabled field must be bool
        """

        assert type(self.api_data['results'][0][self.id]['enabled']) is bool



    def test_api_field_exists_id_created(self):
        """ Test for existance of API Field

        id.created key must exist
        """

        assert 'created' in self.api_data['results'][0][self.id]


    def test_api_field_type_id_created(self):
        """ Test for type for API Field

        id.created field must be datetime
        """

        assert type(self.api_data['results'][0][self.id]['created']) is datetime



    def test_api_field_exists_id_modified(self):
        """ Test for existance of API Field

        id.modified key must exist
        """

        assert 'modified' in self.api_data['results'][0][self.id]


    def test_api_field_type_id_modified(self):
        """ Test for type for API Field

        id.modified field must be datetime
        """

        assert type(self.api_data['results'][0][self.id]['modified']) is datetime



    def test_api_field_exists_pagination_meta_count(self):
        """List view API fields exist

        meta key must exist
        """

        assert 'count' in self.api_data



    def test_api_field_not_exists_display_name(self):
        """Test model field not available

        id.display_name key must not exist on public endpoint as this is
        considered internal data.
        """

        assert 'display_name' not in self.api_data['results'][0][self.id]



    def test_api_field_not_exists_software(self):
        """Test model field not available

        id.software key must not exist on public endpoint as this is
        considered internal data.
        """

        assert 'software' not in self.api_data['results'][0][self.id]



    def test_api_field_not_exists_model_notes(self):
        """Test model field not available

        id.model_notes key must not exist on public endpoint as this is
        considered internal data.
        """

        assert 'model_notes' not in self.api_data['results'][0][self.id]



    def test_api_field_not_exists_model__urls(self):
        """Test model field not available

        id._urls key must not exist on public endpoint as this is
        considered internal data.
        """

        assert '_urls' not in self.api_data['results'][0][self.id]



    def test_api_fields_no_extra(self):
        """Test Privacy check

        privacy is checking to ensure no extra fields are supplied on the
        public endpoint potentially leaking data not required for feature
        flagging.

        check the amount of fields within an object to ensure there are no
        extra fields being added.
        """

        assert len(self.api_data['results'][0][self.id]) == 5



    def test_api_field_exists_pagination_links_next(self):
        """List view API fields exist

        links.next key must exist
        """

        assert 'next' in self.api_data



    def test_api_field_exists_pagination_links_prev(self):
        """List view API fields exist

        links.prev key must exist
        """

        assert 'previous' in self.api_data
