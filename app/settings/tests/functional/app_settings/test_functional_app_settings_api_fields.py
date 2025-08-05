import pytest

from django.db import models
from django.test import Client

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_appsettings
class AppSettingsAPITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs, api_request_permissions
    ):

        item = None

        with django_db_blocker.unblock():

            item = model.objects.get(
                owner_organization = None
            )

            request.cls.item = item

        yield item


    @pytest.fixture( scope = 'class')
    def make_request(self, django_db_blocker,
        request,
        api_request_permissions,
    ):

        client = Client()

        with django_db_blocker.unblock():

            api_request_permissions['user']['view'].is_superuser = True
            api_request_permissions['user']['view'].save()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.get( self.item.get_url() )

        request.cls.api_data = response.data



        item_two = getattr(request.cls, 'item_two', None)

        if item_two:

            response_two = client.get( self.item_two.get_url() )

            request.cls.api_data_two = response_two.data

        else:

            request.cls.api_data_two = {}


        yield



    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes': {
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
            # 'owner_organization': {
            #     'expected': dict
            # },
            # 'owner_organization.id': {
            #     'expected': int
            # },
            # 'owner_organization.display_name': {
            #     'expected': str
            # },
            # 'owner_organization.url': {
            #     'expected': Hyperlink
            # },
            'device_model_is_global': {
                'expected': bool
            },
            'device_type_is_global': {
                'expected': bool
            },
            'manufacturer_is_global': {
                'expected': bool
            },
            'software_is_global': {
                'expected': bool
            },
            'software_categories_is_global': {
                'expected': bool
            },
            'global_organization': {
                'expected': dict
            },
            'global_organization.id': {
                'expected': int
            },
            'global_organization.display_name': {
                'expected': str
            },
            'global_organization.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class AppSettingsAPIInheritedCases(
    AppSettingsAPITestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsAPIPyTest(
    AppSettingsAPITestCases,
):

    pass
