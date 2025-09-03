import pytest

from access.permissions.user import UserPermissions

from api.tests.unit.test_unit_common_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.user_settings import (
    UserSettings,
    ViewSet,
)



@pytest.mark.model_usersettings
class ViewsetTestCases(
    ModelRetrieveUpdateViewSetInheritedCases,
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
                'value': []
            },
            'model': {
                'value': UserSettings
            },
            'model_documentation': {
                'type': type(None),
            },
            'permission_classes': {
                'value': [
                    UserPermissions,
                ]
            },
            # 'queryset': {
            #     'type': type(None),
            # },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Your Settings'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class UserSettingsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsViewsetPyTest(
    ViewsetTestCases,
):

    pass
