import pytest

from django.db import models

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases,
)

from core.models.ticket_base import TicketBase
from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
)



@pytest.mark.tickets
@pytest.mark.model_modelticket
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):

        viewset = ViewSet

        viewset.kwargs = {'model_id': 1}

        yield ViewSet

        del viewset


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
            'base_model': {
                'value': ModelTicket
            },
            'documentation': {
                'type': type(None),
            },
            'filterset_fields': {
                'value': [
                   'ticket',
                   'organization'
                ]
            },
            'metadata_markdown': {
                'value': True
            },
            'model': {
                'value': ModelTicket
            },
            'model_documentation': {
                'type': type(None),
            },
            'model_kwarg': {
                'value': 'model_name'
            },
            'model_suffix': {
                'type': str,
                'value': 'ticket'
            },
            'parent_model': {
                'type': type(None),
                'value': None
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'model_id'
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Models linked to ticket'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



    def test_function_get_parent_model(self, viewset, model):

        viewset = viewset()

        assert viewset.get_parent_model() is None



class ModelTicketViewsetInheritedCases(
    ViewsetTestCases,
):

    @property
    def parameterized_class_attributes(self):
        return {
            'parent_model': {
                'type': models.base.ModelBase,
                'value': TicketBase
            },
        }


    def test_function_get_parent_model(self, viewset, model):

        viewset = viewset()

        viewset.kwargs = {
            viewset.model_kwarg: model._meta.get_field('model').related_model._meta.model_name
        }

        assert viewset.get_parent_model() is model._meta.get_field('model').related_model



@pytest.mark.module_core
class ModelTicketViewsetPyTest(
    ViewsetTestCases,
):


    @pytest.mark.xfail( reason = 'Model requires kwarg model_id' )
    def test_function_get_queryset_manager_calls_user(self, mocker, model, viewset):

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



    def test_function_get_queryset_manager_calls_user_custom_kwarg_model_id(
        self, mocker, model, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  {
            'model_id': 1
        }

        view_set.get_queryset()

        manager.user.assert_called()



    @pytest.mark.xfail( reason = 'Model requires kwarg model_id' )
    def test_function_get_queryset_manager_filters_by_pk(self, mocker, model, viewset):

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'pk': 1
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)



    def test_function_get_queryset_manager_filters_by_pk_custom_kwarg_model_id(
        self, mocker, model, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'pk': 1,
            'model_id': 1
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)



    @pytest.mark.xfail( reason = 'Model requires kwarg model_id' )
    def test_view_func_get_queryset_cache_result(self, mocker, viewset_mock_request):

        view_set = viewset_mock_request
        view_set.kwargs = {
            'model_id': 1
        }
        mocker.patch.object(view_set.model, 'objects', return_value = 'boo')

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as queries:

            assert view_set._queryset is None    # Must be empty before init

            view_set.get_queryset()

            initial_db_queries = len(queries)

            assert view_set._queryset is not None    # Must not be empty after init

            assert len(queries) == initial_db_queries



    def test_view_func_get_queryset_cache_result_custom_kwarg_model_id(
        self, mocker, viewset_mock_request
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        view_set.kwargs = {
            'model_id': 1
        }
        mocker.patch.object(view_set.model, 'objects', return_value = 'boo')

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as queries:

            assert view_set._queryset is None    # Must be empty before init

            view_set.get_queryset()

            initial_db_queries = len(queries)

            assert view_set._queryset is not None    # Must not be empty after init

            assert len(queries) == initial_db_queries



    @pytest.mark.xfail( reason = 'Model requires kwarg model_id' )
    def test_view_func_get_queryset_cache_result_used(self, mocker, viewset, viewset_mock_request):

        view_set = viewset_mock_request

        qs = mocker.spy(view_set.model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        # one call to .all()
        assert initial_method_calls > 0
        # calls = .user( ...), .user().all(), .user().all().filter()
        assert initial_mock_calls > 0

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls



    def test_view_func_get_queryset_cache_result_used_custom_kwarg_model_id(
        self, mocker, viewset, viewset_mock_request
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>._queryset`
        """

        view_set = viewset_mock_request
        view_set.kwargs = {
            'model_id': 1
        }

        qs = mocker.spy(view_set.model, 'objects')

        view_set.get_queryset()    # Initial QuerySet fetch/filter and cache

        initial_method_calls = len(qs.method_calls)
        initial_mock_calls = len(qs.mock_calls)

        # one call to .all()
        assert initial_method_calls > 0
        # calls = .user( ...), .user().all(), .user().all().filter()
        assert initial_mock_calls > 0

        view_set.get_queryset()    # Use Cached results, dont re-fetch QuerySet

        assert len(qs.method_calls) == initial_method_calls
        assert len(qs.mock_calls) == initial_mock_calls
