
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



class TicketCommentSolutionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentSolutionViewsetPyTest(
    ViewsetTestCases,
):

    pass
