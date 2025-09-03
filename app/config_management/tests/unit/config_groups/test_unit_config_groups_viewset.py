import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from config_management.viewsets.config_group import (
    ConfigGroups,
    ViewSet,
)



@pytest.mark.model_configgroups
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
                    'parent'
                ]
            },
            'model': {
                'value': ConfigGroups
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name',
                    'config'
                ]
            },
            'view_description': {
                'value': 'Configuration Groups'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }


    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):

        qs = mocker.spy(viewset_mock_request.model, 'objects')

        viewset_mock_request.get_queryset()    # Initial QuerySet fetch/filter and cache

        assert len(qs.method_calls) == 1       # one call to .all()
        assert len(qs.mock_calls) == 3         # calls = .all(), all().filter()

        viewset_mock_request.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == 1
        assert len(qs.mock_calls) == 3


class KnowledgeBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_config_management
class KnowledgeBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
