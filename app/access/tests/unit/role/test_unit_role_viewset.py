import pytest

from access.viewsets.role import (
    Role,
    ViewSet,
)

from api.tests.unit.test_unit_common_viewset import (
    ModelViewSetInheritedCases
)



@pytest.mark.model_role
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
                'value': None
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
            },
            'filterset_fields': {
                'value': [
                   'organization',
                   'permissions'
                ]
            },
            'model': {
                'value': Role
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
                    'model_notes',
                    'name'
                ]
            },
            'view_description': {
                'value': 'Available Roles'
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
        assert len(qs.mock_calls) == 1         # calls = .all(), all().filter()

        viewset_mock_request.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == 1
        assert len(qs.mock_calls) == 1



class RoleViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class RoleViewsetPyTest(
    ViewsetTestCases,
):
    pass
