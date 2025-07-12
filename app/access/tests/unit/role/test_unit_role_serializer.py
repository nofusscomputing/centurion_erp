import pytest

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
@pytest.mark.module_role
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
