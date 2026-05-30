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

    def test_function_get_meta_urls_self_url(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_no_sub_models_key(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_keys(self):
        pytest.xfail( reason = 'Base class does not require test' )


    def test_function_get_meta_urls_sub_models_values(self,):
        pytest.xfail( reason = 'Base class does not require test' )
