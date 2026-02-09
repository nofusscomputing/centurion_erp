import pytest
import random

from api.tests.unit.test_unit_common_viewset import MockRequest

from core.tests.unit.model_tickets.test_unit_model_tickets_viewset import (
    ModelTicketViewsetInheritedCases
)
from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
)




@pytest.mark.tickets
@pytest.mark.model_modelticketmeta
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


    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset, mocker,
        model_user, kwargs_user, organization_one, model,
        model_instance, model_kwargs, 
    ):

        with django_db_blocker.unblock():

            obj = model_instance( kwargs_create = model_kwargs() )

            kwargs = kwargs_user()
            kwargs['username'] = "test_user1-" + str(
                str(
                    random.randint(1,99))
                    + str(random.randint(300,399))
                    + str(random.randint(400,499)
                )
            ),

            user = model_user.objects.create( **kwargs )

        view_set = viewset()


        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            organization = organization_one,
        )

        view_set.request = request
        view_set.kwargs = obj.get_url_kwargs( many = True )

        yield view_set

        del view_set.request

        with django_db_blocker.unblock():

            user.delete()



    def test_function_get_queryset_manager_calls_user(self, mocker,
        model, model_instance, model_kwargs, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the manager is first called with
        `.user()` so as to ensure that the queryset returns only data the user has
        access to.
        """

        obj = model_instance( kwargs_create = model_kwargs() )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  obj.get_url_kwargs( many = True)

        tester = obj.get_url_kwargs( many = True)

        view_set.get_queryset()

        manager.user.assert_called()


    def test_function_get_queryset_manager_filters_by_pk(self, mocker,
        model, model_instance, model_kwargs, viewset
    ):
        """Test class function

        Ensure that when function `get_queryset` the queryset is filtered by `pk` kwarg
        """

        obj = model_instance( kwargs_create = model_kwargs() )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

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

        obj = model_instance( kwargs_create = model_kwargs() )

        if not model._is_submodel:
            pytest.xfail( reason = 'test case only applicable to sub-models' )

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            **obj.get_url_kwargs( many = True ),
        }

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(
            model_id=view_set.kwargs['model_id']
        )

