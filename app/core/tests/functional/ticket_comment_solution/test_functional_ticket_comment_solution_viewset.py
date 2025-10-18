
import pytest
import random

from api.tests.functional.test_functional_common_viewset import (
    MockRequest
)

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases
)



@pytest.mark.model_ticketcommentsolution
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model, model_ticketcommentbase
    ):

        with django_db_blocker.unblock():

            kwargs = kwargs_user()
            kwargs['username'] = 'username.one' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user = model_user.objects.create( **kwargs )

            kwargs = kwargs_user()
            kwargs['username'] = 'username.two' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user2 = model_user.objects.create( **kwargs )

            self.user = user

            kwargs = model_kwargs()
            del kwargs['external_ref']
            del kwargs['external_system']
            # if 'organization' in kwargs:
            kwargs['organization'] = organization_one
            # if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
            #     kwargs['user'] = user2
            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs['ticket'].status = kwargs['ticket'].TicketStatus.NEW
            kwargs['ticket'].is_solved = False
            kwargs['ticket'].is_closed = False
            kwargs['ticket'].save()

            kwargs = model_kwargs()
            del kwargs['external_ref']
            del kwargs['external_system']
            # if 'organization' in kwargs:
            kwargs['organization'] = organization_two
            # if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
            #     kwargs['user'] = user
            other_tenancy_item = model_instance( kwargs_create = kwargs )

        view_set = viewset()
        model = getattr(view_set, 'model', None)

        if not model:
            model = Tenant

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            tenant = organization_one
        )

        view_set.request = request
        view_set.kwargs = user_tenancy_item.get_url_kwargs( many = True )


        yield view_set

        del view_set.request
        del view_set
        del self.user

        with django_db_blocker.unblock():

            for group in user.groups.all():

                for role in group.roles.all():
                    role.delete()

                group.delete()

            user_tenancy_item.delete()
            other_tenancy_item.delete()

            user.delete()
            user2.delete

            for db_obj in model_user.objects.all():
                try:
                    db_obj.delete()
                except:
                    pass



    def test_function_get_queryset_filtered_results_action_list(self,
        viewset_mock_request, organization_one, organization_two, model
    ):

        viewset = viewset_mock_request

        viewset.action = 'list'

        if not viewset.model:
            pytest.xfail( reason = 'no model exists, assuming viewset is a base/mixin viewset.' )

        only_user_results_returned = True

        queryset = viewset.get_queryset()

        objects = model.objects.all()

        assert len( objects ) >= 2, 'multiple objects must exist for test to work'
        assert len( queryset ) > 0, 'Empty queryset returned. Test not possible'
        if model._meta.model_name != 'tenant':
            assert len(model.objects.filter( organization = organization_one)) > 0, 'objects in user org required for test to work.'
            objects[1].ticket.organization = organization_two
            objects[1].ticket.status = objects[1].ticket.TicketStatus.NEW
            objects[1].ticket.is_solved = False
            objects[1].ticket.is_closed = False
            objects[1].ticket.save()
            objects[1].save()

            assert len(model.objects.filter( organization = organization_two)) > 0, 'objects in different org required for test to work.'


        for result in queryset:

            if result.get_tenant() != organization_one:
                only_user_results_returned = False

        assert only_user_results_returned



class TicketCommentSolutionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentSolutionViewsetPyTest(
    ViewsetTestCases,
):

    pass
