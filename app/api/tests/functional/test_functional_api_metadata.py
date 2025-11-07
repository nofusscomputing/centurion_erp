import pytest

from django.db import models
from django.test import Client

from rest_framework.relations import Hyperlink


@pytest.mark.functional
class APIMetadataTestCases:
    """ API field Rendering Test Suite

    This test suite tests the rendering of API Metadata fieilds.
    """

    @property
    def parameterized_api_metadata_fields(self) -> dict:

        return {
            'name': {
                'expected': str
            },
            'description': {
                'expected': str
            },
            'documentation': {
                'expected': str
            },
            'urls': {
                'expected': dict
            },
            'urls.self': {
                'expected': str
            },

            # 'renders': {
            #     'expected': str
            # },

            # 'parses': {
            #     'expected': str
            # },

            'fields': {
                'expected': dict
            },

            'table_fields': {
                'expected': list
            },
            'layout': {
                'expected': list
            },
            'version': {
                'expected': dict
            },
            'navigation': {
                'expected': list
            },
        }



    @pytest.fixture( scope = 'class')
    def metadata_request(self, api_request_permissions):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.options( self.item.get_url() )


        yield response.data





    @pytest.mark.regression
    def test_api_metadata_field_exists(self, recursearray, metadata_request,
        parameterized, param_key_api_metadata_fields,
        param_value,
        param_expected
    ):
        """Test for existance of API metadata Field"""

        api_data = recursearray(metadata_request, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert api_data['key'] not in api_data['obj']

        else:

            assert api_data['key'] in api_data['obj']



    @pytest.mark.regression
    def test_api_metadata_field_type(self, recursearray, metadata_request,
        parameterized, param_key_api_metadata_fields,
        param_value,
        param_expected
    ):
        """Test for type for API metadata Field"""

        api_data = recursearray(metadata_request, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert api_data['key'] not in api_data['obj']

        else:

            assert type( api_data.get('value', 'is empty') ) is param_expected


@pytest.mark.fields
@pytest.mark.metadata
@pytest.mark.api
class APIMetadataInheritedCases(
    APIMetadataTestCases
):

    pass
