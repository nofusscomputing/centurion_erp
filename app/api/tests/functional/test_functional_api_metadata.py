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

            # Not used for page rendering
            # 'renders': {
            #     'expected': str
            # },

            # Not used for page rendering
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
    def metadata_request_detail(self, api_request_permissions):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.options( self.item.get_url( many = False ) )


        yield response



    @pytest.fixture( scope = 'class')
    def metadata_request_list(self, api_request_permissions):

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.options( self.item.get_url( many = True ) )


        yield response



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_detail_field_exists(self, recursearray, metadata_request_detail,
        parameterized, param_key_api_metadata_fields,
        param_value,
        param_expected
    ):
        """Test for existance of API metadata Field"""

        api_data = recursearray(metadata_request_detail.data, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert api_data['key'] not in api_data['obj']

        else:

            assert api_data['key'] in api_data['obj']



    @pytest.mark.metadata
    def test_api_metadata_detail_field_type(self, recursearray, metadata_request_detail,
        parameterized, param_key_api_metadata_fields,
        param_value,
        param_expected
    ):
        """Test for type for API metadata Field"""

        api_data = recursearray(metadata_request_detail.data, param_value)

        if param_expected is models.NOT_PROVIDED:

            assert api_data['key'] not in api_data['obj']

        else:

            assert type( api_data.get('value', 'is empty') ) is param_expected



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_detail_requires_auth(self):
        """API Metadata check

        Ensure that a detail request to metadata returns HTTP/401 when not
        authenticated
        """

        client = Client()

        response = client.options( self.item.get_url( many = False ) )

        assert response.status_code == 401



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_list_requires_auth(self):
        """API Metadata check

        Ensure that a detail request to metadata returns HTTP/401 when not
        authenticated
        """

        client = Client()

        response = client.options( self.item.get_url( many = True ) )

        assert response.status_code == 401



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_detail_ok(self, metadata_request_detail):
        """API Metadata check

        Ensure that a detail request to metadata returns HTTP/200
        """

        assert metadata_request_detail.status_code == 200



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_list_ok(self, metadata_request_list):
        """API Metadata check

        Ensure that a list request to metadata returns HTTP/200
        """

        assert metadata_request_list.status_code == 200



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_detail_has_layout(self, metadata_request_detail):
        """API Metadata check

        Ensure that a list request contains page layout
        """

        assert 'layout' in metadata_request_detail.data



    @pytest.mark.metadata
    @pytest.mark.regression
    def test_api_metadata_list_has_table_fields(self, metadata_request_list):
        """API Metadata check

        Ensure that a list request contains the table fields
        """

        assert 'table_fields' in metadata_request_list.data








@pytest.mark.fields
@pytest.mark.metadata
@pytest.mark.api
class APIMetadataInheritedCases(
    APIMetadataTestCases
):

    pass
