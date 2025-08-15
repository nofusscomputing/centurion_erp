import pytest

from api.tests.unit.test_unit_common_viewset import (
    ModelRetrieveUpdateViewSetInheritedCases
)

from settings.viewsets.external_link import (
    ExternalLink,
    ViewSet,
)



@pytest.mark.model_externallink
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
                'value': [
                    'cluster',
                    'devices',
                    'service',
                    'software'
                ]
            },
            'model': {
                'value': ExternalLink
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
                'value': 'External Link tags'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ExternalLinkViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_settings
class ExternalLinkViewsetPyTest(
    ViewsetTestCases,
):

    pass
