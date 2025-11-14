import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_ticketcategory
class TicketCategoryModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class TicketCategoryModelInheritedCases(
    TicketCategoryModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketCategoryModelPyTest(
    TicketCategoryModelTestCases,
):
    pass
