import pytest
import random

from types import NoneType

from django.db import models

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    ModelListRetrieveDeleteViewSetInheritedCases
)

from core.viewsets.ticket_dependency import (
    TicketBase,
    TicketDependency,
    ViewSet
)

from api.tests.unit.test_unit_common_viewset import (
    MockRequest
)



@pytest.mark.tickets
@pytest.mark.model_ticketdependency
class ViewsetTestCases(
    ModelListRetrieveDeleteViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': NoneType,
            },
            '_model_documentation': {
                'type': NoneType,
            },
            'back_url': {
                'type': NoneType,
            },
            'documentation': {
                'type': NoneType,
            },
            'filterset_fields': {
                'value': [
                    'organization'
                ]
            },
            'metadata_markdown': {
                'value': True
            },
            'model': {
                'value': TicketDependency
            },
            'model_documentation': {
                'type': NoneType,
            },
            'parent_model': {
                'type': models.base.ModelBase,
                'value': TicketBase
            },
            'parent_model_pk_kwarg': {
                'value': 'ticket_id'
            },
            'search_fields': {
                'value': [
                    'name'
                ]
            },
            'serializer_class': {
                'type': NoneType,
            },
            'view_description': {
                'value': 'Tickets that a dependent upon one another.'
            },
            'view_name': {
                'type': NoneType,
            },
            'view_serializer_name': {
                'type': NoneType,
            },
        }




    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one,
        model_kwargs,
    ):

        with django_db_blocker.unblock():

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
        model = getattr(view_set, 'model', None)

        if not model:
            model = Tenant

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            organization = organization_one
        )

        view_set.request = request

        model_kwargs = model_kwargs()
        view_set.kwargs = {
            'ticket_id': model_kwargs['ticket'].id
        }

        yield view_set

        del view_set.request

        with django_db_blocker.unblock():

            user.delete()



    def test_function_get_parent_model(self, mocker, viewset):

        assert viewset().get_parent_model() is TicketBase



    def test_function_get_queryset_manager_calls_user(self, mocker, model, viewset,
        model_kwargs
    ):

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()
        view_set.request = mocker.Mock()
        view_set.kwargs =  {
            'ticket_id': model_kwargs()['ticket'].id
        }

        if model._is_submodel:
            view_set.kwargs =  {
                view_set.model_kwarg: model._meta.model_name
            }

        view_set.get_queryset()

        manager.user.assert_called()



    def test_function_get_queryset_manager_filters_by_pk(self, mocker, model, viewset,
        model_kwargs
    ):

        manager = mocker.patch.object(model, 'objects' )

        view_set = viewset()

        view_set.request = mocker.Mock()

        view_set.kwargs =  {
            'ticket_id': model_kwargs()['ticket'].id,
            'pk': 1
        }

        if model._is_submodel:
            view_set.kwargs.update({
                view_set.model_kwarg: model._meta.model_name
            })

        view_set.get_queryset()

        manager.user.return_value.all.return_value.filter.assert_called_once_with(pk=1)



class TicketDependencyViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyViewsetPyTest(
    ViewsetTestCases,
):

    pass
