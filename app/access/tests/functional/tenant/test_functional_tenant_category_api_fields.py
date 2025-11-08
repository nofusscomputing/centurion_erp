import pytest

from rest_framework.relations import Hyperlink

from django.db import models
from django.test import Client

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_tenant
class TenantAPITestCases(
    APIFieldsInheritedCases,
):

    @pytest.fixture( scope = 'class')
    def make_request(self, django_db_blocker,
        request, organization_one,
        api_request_permissions,
    ):

        client = Client()

        with django_db_blocker.unblock():

            organization_one.manager = api_request_permissions['user']['view']
            organization_one.model_notes = 'sad'
            organization_one.save()

            client.force_login( api_request_permissions['user']['view'] )
            response = client.get(
                organization_one.get_url()
            )

        request.cls.api_data = response.data



        item_two = getattr(request.cls, 'item_two', None)

        if item_two:

            response_two = client.get( self.item_two.get_url() )

            request.cls.api_data_two = response_two.data

        else:

            request.cls.api_data_two = {}


        yield

        with django_db_blocker.unblock():

            organization_one.manager = None
            organization_one.model_notes = None
            organization_one.save()


    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'organization': {
                'expected': models.NOT_PROVIDED
            },
            'organization.id': {
                'expected': models.NOT_PROVIDED
            },
            'organization.display_name': {
                'expected': models.NOT_PROVIDED
            },
            'organization.url': {
                'expected': models.NOT_PROVIDED
            },
            'name': {
                'expected': str
            },
            'manager': {
                'expected': dict
            },
            'manager.id': {
                'expected': int
            },
            'manager.display_name': {
                'expected': str
            },
            'manager.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class TenantAPIInheritedCases(
    TenantAPITestCases,
):
    pass



@pytest.mark.module_access
class TenantAPIPyTest(
    TenantAPITestCases,
):


    def test_api_metadata_detail_field_exists(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_detail_field_type(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')

    def test_api_metadata_detail_requires_auth(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_list_requires_auth(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_detail_ok(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_list_ok(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_detail_has_layout(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')


    def test_api_metadata_list_has_table_fields(self):
        pytest.skip( reason = 'not required until test_functional_tenant_metadata.py removed')

