import pytest

from rest_framework.test import APIClient

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from core.viewsets.ticket_dependency import (
    ViewSet,
)



@pytest.mark.model_tickets
@pytest.mark.model_ticketdependency
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        clean_model_from_db, api_request_permissions,
        organization_one, organization_two,
        model_instance, model_kwargs, model_ticketcommentbase,
        settings
    ):

        with django_db_blocker.unblock():

            user = api_request_permissions['user']['view']

            user2 = api_request_permissions['user']['change']

            self.user = user

            kwargs = model_kwargs()
            kwargs['user'] = user.employee
            kwargs['ticket'].organization = organization_one
            kwargs['ticket'].save()

            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs = model_kwargs()
            kwargs['ticket'].organization = organization_two
            kwargs['ticket'].save()
            kwargs['user'] = user2.employee

            other_tenancy_item = model_instance( kwargs_create = kwargs )


        settings.SITE_URL = 'http://testserver'

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get(user_tenancy_item.get_url(many = True))

        view_set = response.renderer_context['view']


        yield view_set

        del view_set.request
        del view_set
        del self.user



    def test_function_get_queryset_filtered_results_action_list_ticket(self,
        viewset_mock_request, model, api_request_permissions,
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values that are filtered
        to the ticket in question.
        """

        viewset = viewset_mock_request

        viewset.action = 'list'

        viewset.allowed_methods = [ 'GET' ]

        queryset = viewset.get_queryset()

        assert len(
            model.objects.all()
        ) >= 2, 'multiple objects must exist for test to work'

        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'

        test_obj = model.objects.filter(
            organization = api_request_permissions['tenancy']['user']
        )


        assert len(
            test_obj
        ) > 0, 'objects in user org required for test to work.'

        assert len(
            model.objects.filter(
                organization = api_request_permissions['tenancy']['different']
            )
        ) > 0, 'objects in different org required for test to work.'


        only_user_results_returned = True

        for result in queryset:

            if result.ticket.id != test_obj[0].ticket.id:
                only_user_results_returned = False


        assert only_user_results_returned



class TicketDependencyViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyViewsetPyTest(
    ViewsetTestCases,
):

    pass
