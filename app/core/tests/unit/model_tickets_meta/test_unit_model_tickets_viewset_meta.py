import pytest

from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
)

from core.tests.unit.model_tickets.test_unit_model_tickets_viewset import (
    ModelTicketViewsetInheritedCases
)


@pytest.mark.tickets
@pytest.mark.model_modelticket
class ViewsetTestCases(
    ModelTicketViewsetInheritedCases,
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
            'model': {
                'value': ModelTicket
            },
            'model_documentation': {
                'type': type(None),
            },
            'model_kwarg': {
                'value': 'model_name'
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



class ModelTicketViewsetMetaInheritedCases(
    ViewsetTestCases,
):


    def test_function_get_queryset_manager_calls_user(self, mocker,
        model, model_instance, model_kwargs, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        obj = model_instance( kwargs_create = model_kwargs )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  obj.get_url_kwargs( many = True)

        tester = obj.get_url_kwargs( many = True)

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.get_queryset()

        manager.user.assert_called()


    def test_function_get_queryset_manager_filters_by_pk(self, mocker,
        model, model_instance, model_kwargs, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        obj = model_instance( kwargs_create = model_kwargs )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            **obj.get_url_kwargs(),
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(
            model_id = view_set.kwargs['model_id'], pk = view_set.kwargs['pk']
        )


    def test_function_get_queryset_manager_filters_by_model_id(self, mocker,
        model, model_instance, model_kwargs, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `.model_kwarg` kwarg
        """

        obj = model_instance( kwargs_create = model_kwargs )

        if not model._is_submodel:
            pytest.xfail( reason = 'test case only applicable to sub-models' )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        mocker.patch.object(view_set, 'get_permission_required', return_value = None)

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            **obj.get_url_kwargs( many = True ),
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(
            model_id=view_set.kwargs['model_id']
        )

