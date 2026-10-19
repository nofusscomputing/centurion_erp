import pytest

from rest_framework.exceptions import ParseError, ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView


@pytest.mark.model_role
class RoleSerializerTestCases(
    SerializerTestCases
):

    def test_serializer_validation_no_name(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['name']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_function_to_internal_value_permissions_as_int(self,
        mocker, model_serializer
    ):
        """Serializer Function Check

        Ensure that function `to_internal_value` accepts permissions as a list
        of int, i.e. the string-to-id conversion is not attempted.
        """

        serializer = model_serializer['model']()

        permission_model = serializer.Meta.model.permissions.field.related_model

        permission_objects = mocker.patch.object(permission_model, 'objects')

        mocker.patch(
            'rest_framework.serializers.ModelSerializer.to_internal_value'
        )

        serializer.to_internal_value({ 'permissions': [ 1, 2 ] })

        permission_objects.filter.assert_not_called()



    def test_serializer_function_to_internal_value_permissions_to_int(self,
        mocker, model_serializer
    ):
        """Serializer Function Check

        Ensure that function `to_internal_value` converts the permission
        strings list to a list of int.
        """

        serializer = model_serializer['model']()

        permission_model = serializer.Meta.model.permissions.field.related_model

        permission = mocker.Mock()
        permission.id = 99

        permission_objects = mocker.patch.object(permission_model, 'objects')
        permission_objects.filter.return_value = [ permission ]

        mocker.patch(
            'rest_framework.serializers.ModelSerializer.to_internal_value'
        )

        data = { 'permissions': [ 'app_label.codename' ] }

        serializer.to_internal_value( data )

        assert data['permissions'] == [ 99 ]



    def test_serializer_function_to_internal_value_permissions_not_exist(self,
        mocker, model_serializer
    ):
        """Serializer Function Check

        Ensure that function `to_internal_value` raises an exception when a
        permission supplied does not exist.
        """

        serializer = model_serializer['model']()

        permission_model = serializer.Meta.model.permissions.field.related_model

        permission_objects = mocker.patch.object(permission_model, 'objects')
        permission_objects.filter.return_value = []

        with pytest.raises(ParseError) as exception:

            serializer.to_internal_value({ 'permissions': [ 'app_label.codename' ] })

        assert exception.value.get_codes() == 'supplied_permission_does_not_exist'



class RoleSerializerInheritedCases(
    RoleSerializerTestCases
):
    pass



@pytest.mark.module_access
class RoleSerializerPyTest(
    RoleSerializerTestCases
):
    pass



# from pytest import MonkeyPatch

# from unittest.mock import patch

# from access.functions import permissions

# from access.serializers import role

# def mock_func(**kwargs):
#     return 'is_called'


###############################################################################
#
# This test works when run alone, however not when all unit tests are run
# need to figure out how to correctly isolate the test.
#
###############################################################################


@pytest.mark.model_role
@pytest.mark.model_role
@pytest.mark.skip( reason = 'figure out how to isolate so entirety of unit tests can run without this test failing' )
# @pytest.mark.forked
# @pytest.mark.django_db
# @patch("access.functions.permissions.permission_queryset", return_value='no_called', side_effect=mock_func)
# @patch.object(role, "permission_queryset", return_value='no_called', side_effect=mock_func)
# @patch.object(permissions, "permission_queryset", return_value='no_called', side_effect=mock_func)
# @patch.object(role, "permission_queryset", side_effect=mock_func)
# @patch.object(globals()['role'], "permission_queryset", return_value='no_called', side_effect=mock_func)
# @patch.object(globals()['role'], "permission_queryset", side_effect=mock_func)
# @pytest.mark.forked    # from `pip install pytest-forked`
# def test_serializer_field_permission_uses_permissions_selector(mocked_obj):
def test_serializer_field_permission_uses_permissions_selector(mocker):
# def test_serializer_field_permission_uses_permissions_selector(monkeypatch):
    """Field Permission Check

    field `permission` must be called with `queryset=access.functions.permissions.permission_queryset()`
    so that ONLY the designated permissions are visible
    """

    def mock_func(**kwargs):
        return 'is_called'

    mocker.patch("access.functions.permissions.permission_queryset", return_value='no_called', side_effect=mock_func)

    from access.serializers import role
    # from access.serializers.role import permission_queryset, ModelSerializer

    # monkey = MonkeyPatch().setattr(role, 'permission_queryset', mock_func)

    # monkeypatch.setattr(role, 'permission_queryset', mock_func)
    # monkey = MonkeyPatch.setattr('access.functions.permissions.permission_queryset', mock_func)
    # monkeypatch.setattr(permissions, 'permission_queryset', mock_func)

    serializer = role.ModelSerializer()

    # if `return_value` exists, the function was not called
    assert getattr(serializer.fields.fields['permissions'].child_relation.queryset, 'return_value', None) is None

    #if `queryset == is_called` the function was called
    assert serializer.fields.fields['permissions'].child_relation.queryset == 'is_called'
