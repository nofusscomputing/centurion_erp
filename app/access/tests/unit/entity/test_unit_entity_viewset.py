import pytest
import logging

from access.viewsets.entity import (
    Entity,
    NoDocsViewSet,
    ViewSet,
)

from api.tests.unit.test_unit_common_viewset import SubModelViewSetInheritedCases



@pytest.mark.model_entity
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': logging.Logger,
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'base_model': {
                'value': Entity
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'organization'
                ]
            },
            'model': {
                'value': Entity
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'model_kwarg': {
                'value': 'model_name'
            },
            'model_suffix': {
                'type': type(None)
            },
            'queryset': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'search_fields': {
                'value': [
                    'model_notes'
                ]
            },
            'view_description': {
                'value': 'All entities'
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }



@pytest.mark.skip(reason = 'see #895, tests being refactored')
class EntityViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class EntityViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
