import pytest

from django.db.models import ObjectDoesNotExist
from rest_framework import serializers

from centurion.tests.unit_class import ClassTestCases

from core.fields.markdown import MarkdownField



# ToDo: Add Testsuite for model rendering tests to be included within every models functional tests
# ToDo: Add Test Suite for ticket rendering to be included within every ticket models function tests.
#
# Must:
#   - confirm permission
#   - correct rendering dict
#   - correct model
#   - no model, empty render dict
#   - missing permission, empty render dict



@pytest.mark.api
@pytest.mark.fields
@pytest.mark.markdown
@pytest.mark.serializer
@pytest.mark.unit
class MarkdownFieldTestCases(
    ClassTestCases
):


    @pytest.fixture( scope = 'class')
    def test_class(self):

        yield MarkdownField



    @property
    def parameterized_class_attributes(self):
        return {
            '__init__': {
                'arg_names': [
                    'self',
                    'multiline',
                    'style_class',
                    'kwargs'
                ],
                'function': True,
            },
            'get_model': {
                'arg_names': [
                    'self',
                    'model_tag'
                ],
                'function': True,
            },
            'get_markdown_render': {
                'arg_names': [
                    'self',
                    'markdown'
                ],
                'function': True,
            },
            'to_representation': {
                'arg_names': [
                    'self',
                    'value'
                ],
                'function': True,
            },
            'style_class': {
                'type': type(None),
                'value': None
            }
        }


    @pytest.fixture(scope = 'class')
    def mock_field_permission(self):

        class MockUser:

            def has_perm(self, **kwargs):
                return True


        class MockRequest:
            user = MockUser()


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
    def mock_field_missing_permission(self):

        class MockUser:

            def has_perm(self, **kwargs):
                return False


        class MockRequest:
            user = MockUser()


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



    def test_function_to_representation_calls_get_markdown_render(self,
        mocker, mock_field_permission
    ):
        """Test Function

        Ensure that function to_representation calls function
        get_markdown_render.
        """


        get_markdown_render = mocker.patch.object(mock_field_permission, 'get_markdown_render', return_value = 'the value')

        markdown = f'a random $model_tag-999999'

        returned_data = mock_field_permission.to_representation(
            value = markdown
        )

        get_markdown_render.assert_called_once_with(markdown = markdown)



    def test_function_get_markdown_render_has_permission_ticket(self,
        mocker, mock_field_permission, model_ticketbase
    ):
        """Test Function

        Ensure that function get_markdown_render returns rendered data if the user has
        permission.
        """


        mocker.patch.object(mock_field_permission, 'get_model', return_value = 'model')

        title = 'a-title'
        url = 'a-url'

        mock_model = model_ticketbase()

        mock_model.id = 999999
        mock_model.status = mock_model.TicketStatus.NEW
        mock_model.ticket_type = 'request'
        mock_model.title = title


        mocker.patch.object(mock_model, 'get_url', return_value = url)
        mocker.patch.object(model_ticketbase.objects, 'get', return_value = mock_model)

        markdown = f'a random #999999'

        assert mock_field_permission.get_markdown_render(
            markdown = markdown
        )['render'] == {
            'tickets':{
                '999999':{
                    'status': mock_model.TicketStatus(mock_model.status).label,
                    'ticket_type': mock_model.ticket_type,
                    'title': str(mock_model),
                    'url': url
                }
            }
        }



    def test_function_get_markdown_render_missing_permission_ticket(self,
        mocker, mock_field_missing_permission, model_ticketbase
    ):
        """Test Function

        Ensure that function get_markdown_render returns no rendered data if the user
        does not have the required permission when model is ticket.
        """


        mocker.patch.object(
            mock_field_missing_permission, 'get_model', return_value = model_ticketbase
        )


        mock_model = model_ticketbase()

        mocker.patch.object(model_ticketbase.objects, 'get', return_value = mock_model)


        markdown = f'a random #1'

        assert mock_field_missing_permission.get_markdown_render(
            markdown = markdown
        )['render'] == {}



    def test_function_get_markdown_render_no_markdown(self,
        mock_field_permission
    ):
        """Test Function

        Ensure that function get_markdown_render returns no rendered data if
        there is no renderable markdown.
        """


        markdown = f'no markdown for rendering'

        assert mock_field_permission.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown,
            'render': {}
        }



@pytest.mark.unit
class MarkdownFieldModelTestCases:
    """Model Test Suite for Markdown Field
    
    This test suite is intended to be included within model test suites.
    """


    @pytest.fixture(scope = 'class')
    def mock_field_permission(self, model):

        class MockUser:

            def has_perm(self, **kwargs):

                if kwargs['permission'] == f"{model._meta.app_label}.view_{model._meta.model_name}":
                    return True

                return False


        class MockRequest:
            user = MockUser()


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
    def mock_field_missing_permission(self):

        class MockUser:

            def has_perm(self, **kwargs):
                return False


        class MockRequest:
            user = MockUser()


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
    def mock_field_permission_wrong_org(self, model, organization_one):

        class MockUser:

            def has_perm(self, **kwargs):

                if(
                    kwargs['permission'] == f"{model._meta.app_label}.view_{model._meta.model_name}"
                    and kwargs['tenancy'] == organization_one
                ):
                    return False

                return True


        class MockRequest:
            user = MockUser()


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
    def test_field_markdown_function_get_model(self, model,
        mock_field_permission
    ):
        """Test Function

        Ensure that function get_model returns the correct model:
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )

        expected_model = model

        if model._is_submodel:

            expected_model = model()._base_model


        assert mock_field_permission.get_model(model_tag = model.model_tag) == expected_model



    @pytest.mark.api
    @pytest.mark.fields
    @pytest.mark.markdown
    @pytest.mark.models
    @pytest.mark.serializer
    def test_field_markdown_function_get_markdown_render_has_permission(self, model,
        mocker, mock_field_permission
    ):
        """Test Function

        Ensure that function get_model returns rendered data if the user has
        permission.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )

        mocker.patch.object(mock_field_permission, 'get_model', return_value = model)

        title = 'a-title'
        url = 'a-url'


        mock_model = model()
        mock_model.title = title

        mocker.patch.object(model.objects, 'get', return_value = mock_model)

        mocker.patch.object(model, '__str__', return_value = title)
        mocker.patch.object(model, 'get_url', return_value = url)

        markdown = f'a random ${model.model_tag}-999999'

        assert mock_field_permission.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {
                'models':{
                    model.model_tag: {
                        '999999':{
                            'title': title,
                            'url': url
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
    def test_field_markdown_function_get_markdown_render_has_permission_obj_exists(self, model,
        mocker, mock_field_permission
    ):
        """Test Function

        Ensure that function get_markdown_render returns no render data if the
        the object is found.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )

        mocker.patch.object(mock_field_permission, 'get_model', return_value = model)

        title = 'a-title'
        url = 'a-url'

        mock_model = model()
        mock_model.title = title

        mocker.patch.object(model.objects, 'get', return_value = mock_model)

        mocker.patch.object(model, '__str__', return_value = title)
        mocker.patch.object(model, 'get_url', return_value = url)

        markdown = f'a random ${model.model_tag}-999999'

        assert mock_field_permission.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {
                'models':{
                    model.model_tag: {
                        '999999':{
                            'title': title,
                            'url': url
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
    def test_field_markdown_function_get_markdown_render_has_permission_obj_not_exist(self, model,
        mocker, mock_field_permission
    ):
        """Test Function

        Ensure that function get_markdown_render returns no render data if the
        the object is not found.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )

        mocker.patch.object(mock_field_permission, 'get_model', return_value = model)

        mocker.patch.object(model.objects, 'get', side_effect = model.DoesNotExist())

        markdown = f'a random ${model.model_tag}-999999'

        assert mock_field_permission.get_markdown_render(
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
        mocker, organization_one, mock_field_permission_wrong_org
    ):
        """Test Function

        Ensure that function get_markdown_render returns no render data if the
        user does not have the permission in the correct org.
        """

        if getattr(model, 'model_tag', None) is None:
            pytest.xfail( reason = 'Model does not have a model_tag. test is N/A.' )

        mocker.patch.object(mock_field_permission_wrong_org, 'get_model', return_value = model)


        mock_model = model()

        mocker.patch.object(model.objects, 'get', return_value = mock_model)
        mocker.patch.object(model, 'get_organization', return_value = organization_one)


        markdown = f'a random ${model.model_tag}-999999'

        assert mock_field_permission_wrong_org.get_markdown_render(
            markdown = markdown
        ) == {
            'markdown': markdown, 
            'render': {}
        }



@pytest.mark.module_core
class MarkdownFieldPyTest(
    MarkdownFieldTestCases
):
    pass