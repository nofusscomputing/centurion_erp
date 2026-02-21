import pytest

from rest_framework import serializers

from core.fields.markdown import MarkdownField



@pytest.mark.functional
class MarkdownFieldModelTestCases:
    """Model Test Suite for Markdown Field
    
    This test suite is intended to be included within model test suites.
    """



    @pytest.fixture(scope = 'class')
    def mock_field(self,
        api_request_permissions,
        model,
    ):


        class MockRequest:
            user = api_request_permissions['user']['view']


        class MockSerializer(serializers.Serializer):

            markdown_field = MarkdownField()


        serializer = MockSerializer(
            {
                'markdown_field': 'data for the field'
            },
            context = {
                'request': MockRequest()
            }
        )

        field = serializer.fields["markdown_field"]

        yield field



    @pytest.fixture(scope = 'class')
    def mock_field_different_tenancy(self,
        api_request_permissions,
        model,
    ):


        class MockRequest:
            user = api_request_permissions['user']['different_tenancy']


        class MockSerializer(serializers.Serializer):

            markdown_field = MarkdownField()


        serializer = MockSerializer(
            {
                'markdown_field': 'data for the field'
            },
            context = {
                'request': MockRequest()
            }
        )

        field = serializer.fields["markdown_field"]

        yield field



    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_has_permission(self, model,
        mock_field, created_model
    ):
        """Test Function

        Ensure that function get_markdown_render returns rendered data if the user has
        permission.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        markdown = f'a random ${created_model.model_tag}-{created_model.id}'

        assert mock_field.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {
                'models':{
                    created_model.model_tag: {
                        str(created_model.id):{
                            'title': str(created_model),
                            'url': str(created_model.get_url( relative = True )).replace('/api/v2', '')
                        }
                    }
                }
            }
        }



    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_has_permission_invalid_Tag(self, model,
        mock_field, created_model
    ):
        """Test Function

        Ensure that function get_markdown_render returns rendered data if the user has
        permission.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        markdown = f'a random ${created_model.model_tag}s-{created_model.id}'

        assert mock_field.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {}
        }



    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_has_permission_obj_not_exist(self, model,
        mock_field, created_model
    ):
        """Test Function

        Ensure that function get_markdown_render returns no render data if the
        the object is not found.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        markdown = f'a random ${created_model.model_tag}-999999999'

        assert mock_field.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {}
        }



    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_wrong_org_permission(self, model,
        mock_field_different_tenancy, created_model
    ):
        """Test Function

        Ensure that function get_markdown_render returns no render data if the
        user does not have the permission in the correct org.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        markdown = f'a random ${created_model.model_tag}-{created_model.id}'

        assert mock_field_different_tenancy.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {}
        }
