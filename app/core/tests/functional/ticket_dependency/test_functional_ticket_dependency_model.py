import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_tickets
@pytest.mark.model_ticketdependency
class TicketDependencyModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class TicketDependencyModelInheritedCases(
    TicketDependencyModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketDependencyModelPyTest(
    TicketDependencyModelTestCases,
):
    pass
