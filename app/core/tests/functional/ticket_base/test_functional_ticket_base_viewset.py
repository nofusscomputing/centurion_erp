
import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.viewsets.ticket import (
    ViewSet,
)



@pytest.mark.model_ticketbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class TicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
