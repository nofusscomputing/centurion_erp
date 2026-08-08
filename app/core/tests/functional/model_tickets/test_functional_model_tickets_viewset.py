import pytest

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from core.viewsets.ticket_model_link import (
    ViewSet,
)



@pytest.mark.tickets
@pytest.mark.model_modelticket
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class ModelTicketViewsetInheritedCases(
    ViewsetTestCases,
):



    @pytest.fixture( scope = 'function' )
    def viewset_mock_request_ticket(self, django_db_blocker,
        model_instance, api_request_permissions, model_kwargs, model,
        model_ticketcommentbase, kwargs_ticketbase, settings,
        model_permission, model_contenttype
    ):

        with django_db_blocker.unblock():

            user = api_request_permissions['user']['view']

            kwargs = model_kwargs()
            kwargs['organization'] = api_request_permissions['tenancy']['user']

            if kwargs['model']._meta.model_name == 'tenant':
                kwargs['model'] = api_request_permissions['tenancy']['user']

            user_tenancy_item = model_instance( kwargs_create = kwargs )

            view_permission_model = model_permission.objects.get(
                codename = 'view_' + user_tenancy_item._base_model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = user_tenancy_item._base_model._meta.app_label,
                    model = user_tenancy_item._base_model._meta.model_name,
                )
            )

            list(list(user.groups.all())[0].roles.all())[0].permissions.add(
                view_permission_model
            )

            kwargs = model_kwargs( organization = api_request_permissions['tenancy']['different'])

            kwargs_ticket = kwargs_ticketbase()
            kwargs_ticket['title'] = 'other org ticket'
            kwargs_ticket['organization'] = api_request_permissions['tenancy']['different']

            kwargs['ticket'] = kwargs['ticket'].__class__.objects.create(
                **kwargs_ticket
            )

            kwargs['organization'] = api_request_permissions['tenancy']['different']

            if hasattr(kwargs['model'], 'organization'):

                kwargs['model'].organization = api_request_permissions['tenancy']['different']

            elif kwargs['model']._meta.model_name == 'tenant':

                kwargs['model'] = api_request_permissions['tenancy']['different']


            kwargs['model'].save()

            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user


            other_tenancy_item = model_instance( kwargs_create = kwargs )


        settings.SITE_URL = 'http://testserver'


        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse(
            viewname = "v2:_api_modelticket-list",
            request = None,
            kwargs = {
                'model_name': user_tenancy_item.ticket._meta.model_name,
                'model_id': user_tenancy_item.ticket.pk,
            }
        )

        response = client.get(
            path = url
        )

        assert response.status_code == 200, "Response was not success, test cant continue."

        view_set = response.renderer_context['view']

        yield view_set

        del view_set.request
        del view_set

        # reset user object caching (fixture is class scoped)
        user._global_organization = None
        user._group_permissions = False
        user._tenancies = None
        user._tenancies_int = None
        user._permissions = None
        user._permissions_by_tenancy = None



    def test_function_get_queryset_filtered_results_action_list_for_ticket(self,
        viewset_mock_request_ticket, model,api_request_permissions,
    ):
        """Test class function

        Ensure that when function `get_queryset` returns values thay are
        filtered to the model in question.

        This test is for `list` of base model for all models related to ticket.
        """

        viewset = viewset_mock_request_ticket

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


        if model._meta.model_name != 'tenant':

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



@pytest.mark.module_core
class ModelTicketViewsetPyTest(
    ViewsetTestCases,
):


    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'test n/a as model does not have `model` field' )

    def test_function_get_meta_urls_self_url(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_no_sub_models_key(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_keys(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_values(self,):
        pytest.xfail( reason = 'Base class does not require test' )
