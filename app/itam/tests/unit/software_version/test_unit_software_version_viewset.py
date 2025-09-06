import pytest

from django.db import models

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.software_version import (
    Software,
    SoftwareVersion,
    ViewSet,
)



@pytest.mark.model_softwareversion
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
                    'software'
                ]
            },
            'model': {
                'value': SoftwareVersion
            },
            'model_documentation': {
                'type': type(None),
            },
            'parent_model': {
                'type': models.base.ModelBase,
                'value': Software
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'software_id'
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
                'value': 'Physical Softwares'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() is not None



    def test_view_func_get_queryset_cache_result(self, mocker, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.kwargs = {
            'software_id': self.kwargs_create_item['software'].id
        }

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset



    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.kwargs = {
            'software_id': self.kwargs_create_item['software'].id
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



    def test_function_get_queryset_manager_calls_user(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  {
                'software_id': self.kwargs_create_item['software'].id
        }

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.get_queryset()

        manager.user.assert_called()


    def test_function_get_queryset_manager_filters_by_pk(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'pk': 1,
            'software_id': self.kwargs_create_item['software'].id
        }

        if model._is_submodel:
            view_set.kwargs.update({
                view_set.model_kwarg: model._meta.model_name
            })

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)



class SoftwareVersionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareVersionViewsetPyTest(
    ViewsetTestCases,
):

    pass
