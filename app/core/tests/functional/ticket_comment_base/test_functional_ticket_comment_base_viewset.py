
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket_comment import (
    ViewSet,
)



@pytest.mark.model_ticketcommentbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



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
            objects[1].ticket.save()
            objects[1].save()
            assert len(model.objects.filter( organization = organization_two)) > 0, 'objects in different org required for test to work.'


        for result in queryset:

            if result.get_tenant() != organization_one:
                only_user_results_returned = False

        assert only_user_results_returned



class TicketCommentBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
