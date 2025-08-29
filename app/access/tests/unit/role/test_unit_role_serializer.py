import pytest

from rest_framework.exceptions import ValidationError

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
