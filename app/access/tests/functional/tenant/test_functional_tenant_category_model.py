import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_tenant
class TenantModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):

    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_has_permission(self, model,
        mock_field, api_request_permissions,
    ):

        created_model = api_request_permissions['tenancy']['user']

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
        mock_field, api_request_permissions,
    ):

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        created_model = api_request_permissions['tenancy']['user']

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
        mock_field, api_request_permissions,
    ):

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        created_model = api_request_permissions['tenancy']['user']

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

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )


        markdown = f'a random ${created_model.model_tag}-{created_model.id}'

        assert mock_field_different_tenancy.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {}
        }



class TenantModelInheritedCases(
    TenantModelTestCases,
):
    pass



@pytest.mark.module_access
class TenantModelPyTest(
    TenantModelTestCases,
):
    pass
