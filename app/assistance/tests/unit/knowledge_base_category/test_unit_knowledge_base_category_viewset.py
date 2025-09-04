import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from assistance.viewsets.knowledge_base_category import (
    KnowledgeBaseCategory,
    ViewSet,
)



@pytest.mark.model_knowledgebasecategory
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
                    'name',
                    'organization',
                    'parent_category',
                    'target_user',
                    'target_team'
                ]
            },
            'model': {
                'value': KnowledgeBaseCategory
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name'
                ]
            },
            'view_description': {
                'value': 'Settings, Knowledge Base Categories'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class knowledgebaseCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgebaseCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass
