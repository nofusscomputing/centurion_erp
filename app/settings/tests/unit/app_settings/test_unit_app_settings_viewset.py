import pytest

from api.tests.unit.test_unit_common_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.app_settings import (
    AppSettings,
    ViewSet,
)



@pytest.mark.model_appsettings
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
                'value': AppSettings
            },
            'model_documentation': {
                'type': type(None),
            },
            'queryset': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Centurion Settings'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class AppSettingsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsViewsetPyTest(
    ViewsetTestCases,
):

    pass
