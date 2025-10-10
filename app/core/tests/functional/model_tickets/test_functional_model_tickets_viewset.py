import pytest



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
    pass



@pytest.mark.module_core
class ModelTicketViewsetPyTest(
    ViewsetTestCases,
):


    def test_function_get_queryset_filtered_results_action_list(self):
        pytest.xfail( reason = 'test n/a as model does not have `model` field' )
