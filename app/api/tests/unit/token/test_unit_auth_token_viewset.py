import pytest

from access.permissions.user import UserPermissions

from api.tests.unit.test_unit_common_viewset import (
    ModelCreateViewSetInheritedCases,
    ModelListRetrieveDeleteViewSetInheritedCases,
)

from api.viewsets.auth_token import (
    AuthToken,
    ViewSet,
)



@pytest.mark.model_authtoken
class ViewsetTestCases(
    ModelCreateViewSetInheritedCases,
    ModelListRetrieveDeleteViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
            },
            '_model_documentation': {
                'type': type(None),
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'expires'
                ]
            },
            'model': {
                'value': AuthToken
            },
            'model_documentation': {
                'type': type(None),
            },
            'permission_classes': {
                'value': [
                    UserPermissions,
                ]
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'note'
                ]
            },
            'view_description': {
                'value': 'User Authentication Tokens'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class AuthTokenViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_api
class AuthTokenViewsetPyTest(
    ViewsetTestCases,
):

    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        qs = mocker.spy(viewset_mock_request.model, 'objects')

        viewset_mock_request.get_queryset()    # Initial QuerySet fetch/filter and cache

        assert len(qs.method_calls) == 1       # one call to .all()
        assert len(qs.mock_calls) == 3         # calls = .all(), all().filter()

        viewset_mock_request.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == 1
        assert len(qs.mock_calls) == 3