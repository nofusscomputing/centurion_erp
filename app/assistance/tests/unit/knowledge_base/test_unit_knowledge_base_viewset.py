import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from assistance.viewsets.knowledge_base import (
    KnowledgeBase,
    ViewSet,
)



@pytest.mark.model_knowledgebase
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
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
                    'organization',
                    'category',
                    'target_user',
                    'target_team',
                    'responsible_user',
                    'responsible_teams',
                    'public'
                ]
            },
            'model': {
                'value': KnowledgeBase
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
                'value': [
                    'title',
                    'summary',
                    'content'
                ]
            },
            'view_description': {
                'value': 'Information Management Knowledge Base Article(s)'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class KnowledgeBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_assistance
class KnowledgeBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
