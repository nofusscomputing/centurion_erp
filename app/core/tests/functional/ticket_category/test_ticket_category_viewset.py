import pytest

from api.tests.functional.viewset.test_functional_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from core.viewsets.ticket_category import (
    ViewSet,
)



@pytest.mark.model_ticketcategory
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class TicketCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass
