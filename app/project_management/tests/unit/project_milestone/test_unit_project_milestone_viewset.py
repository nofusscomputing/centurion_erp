import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from project_management.viewsets.project_milestone import (
    ProjectMilestone,
    ViewSet,
)



@pytest.mark.model_projectmilestone
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
                'value': []
            },
            'model': {
                'value': ProjectMilestone
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
                    'description'
                ]
            },
            'view_description': {
                'value': 'Physical Devices'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }


    def test_view_func_get_queryset_cache_result(self, viewset_mock_request,
        model_kwargs
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        view_set.kwargs = { 'project_id': model_kwargs['project'].id }

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset



    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request,
        model_kwargs,
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request

        view_set.kwargs = {
            'project_id': model_kwargs['project'].id
        }

        qs = mocker.spy(view_set.model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        assert initial_method_calls > 0       # one call to .all()
        assert initial_mock_calls > 0         # calls = .user( ...), .user().all(), .user().all().filter()

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls



class ProjectMilestoneViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectMilestoneViewsetPyTest(
    ViewsetTestCases,
):

    pass
