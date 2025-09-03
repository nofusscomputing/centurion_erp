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

    pass