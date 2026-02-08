import pytest



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



    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'model is not multi-tenancy capable, test is N/A.' )



class TicketDependencyViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyViewsetPyTest(
    ViewsetTestCases,
):

    pass
