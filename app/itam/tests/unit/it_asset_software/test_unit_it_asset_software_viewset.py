import pytest

from itam.models import ITAssetSoftware
from itam.viewsets.it_asset_related import ViewSet


from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    ModelViewSetInheritedCases
)

@pytest.mark.model_itassetoperatingsystem
class ITAssetSoftwareViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self, model):

        viewset = ViewSet

        viewset.kwargs = {
            'model_name': 'itasset',
            # 'related_model_name': model._meta.model_name
            'related_model_name': 'software'
        }
        yield viewset

        del viewset.kwargs


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'value': ITAssetSoftware
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'parent_model_pk_kwarg': {
                'value': 'model_id'
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
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


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'parent model is itasset.' )
    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() is None


    def test_function_get_parent_model_itasset(self, model_itasset, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() == model_itasset


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'calls .user on parent model.' )
    def test_function_get_queryset_manager_calls_user(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  {}

        if model._is_submodel:
            view_set.kwargs =  {
                view_set.model_kwarg: model._meta.model_name
            }

        view_set.get_queryset()

        manager.user.assert_called()


    def test_function_get_queryset_manager_calls_user_parent_model(self, mocker, model_itasset, viewset):
        """Test class function
    
        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs['model_id'] = 1
        
        manager = mocker.patch.object(model_itasset, 'objects' )
    
        view_set.get_queryset()

        manager.user.assert_called()


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'calls .user on parent model.' )
    def test_function_get_queryset_manager_filters_by_pk(self, mocker, model, viewset):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'pk': 1
        }

        if model._is_submodel:
            view_set.kwargs.update({
                view_set.model_kwarg: model._meta.model_name
            })

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)



    def test_function_get_queryset_manager_filters_by_pk_user_parent_model(self,
        mocker, model, viewset, model_itasset, kwargs_itasset,
    ):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs['model_id'] = model_itasset.objects.create( **kwargs_itasset() ).id
        view_set.kwargs['pk'] = 1
        
        manager = mocker.patch.object(model, 'objects' )

        # if model._is_submodel:
        #     view_set.kwargs.update({
        #         view_set.model_kwarg: model._meta.model_name
        #     })

        view_set.get_queryset()

        manager.filter.return_value.filter.assert_called_once_with(pk=1)


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'calls .user on parent model.' )
    def test_view_func_get_queryset_cache_result(self, mocker, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        mocker.patch.object(view_set.model, 'objects', return_value = 'boo')

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as queries:

            assert view_set._queryset is None    # Must be empty before init

            q = view_set.get_queryset()

            evaluate = len(view_set.get_queryset())

            initial_db_queries = len(queries)

            assert view_set._queryset is not None    # Must not be empty after init

            assert len(queries) == initial_db_queries



    def test_view_func_get_queryset_cache_result_parent_model(self,
        mocker, model, viewset_mock_request, model_itasset, kwargs_itasset,
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        view_set.request = mocker.Mock()

        view_set.kwargs['model_id'] = model_itasset.objects.create( **kwargs_itasset() ).id

        mocker.patch.object(model, 'objects')

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as queries:

            assert view_set._queryset is None    # Must be empty before init

            q = view_set.get_queryset()

            evaluate = len(view_set.get_queryset())

            initial_db_queries = len(queries)

            assert view_set._queryset is not None    # Must not be empty after init

            assert len(queries) == initial_db_queries


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'calls .user on parent model.' )
    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request

        qs = mocker.spy(view_set.model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        assert initial_method_calls > 0       # one call to .all()
        assert initial_mock_calls > 0         # calls = .user( ...), .user().all(), .user().all().filter()

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls



    def test_view_func_get_queryset_cache_result_used_parent_model(self,
        mocker, model, viewset_mock_request, model_itasset, kwargs_itasset,
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        view_set.request = mocker.Mock()

        view_set.kwargs['model_id'] = model_itasset.objects.create( **kwargs_itasset() ).id

        qs = mocker.spy(model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        assert initial_method_calls > 0       # one call to .all()
        assert initial_mock_calls > 0         # calls = .user( ...), .user().all(), .user().all().filter()

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls



class ITAssetSoftwareViewsetInheritedCases(
    ITAssetSoftwareViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareViewsetPyTest(
    ITAssetSoftwareViewsetTestCases,
):

    pass
