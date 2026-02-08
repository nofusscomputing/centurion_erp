
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


    def test_function_get_queryset_filtered_results_action_list(self, mocker,
        viewset_mock_request, organization_one, organization_two, model
    ):

        viewset = viewset_mock_request

        viewset.action = 'list'
        viewset.permissions_required = [    # Perms check not done, so populate
            f'{model._meta.app_label}.view_{model._meta.model_name}'
        ]


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
