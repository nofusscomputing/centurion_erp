import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)


@pytest.mark.tickets
@pytest.mark.model_modelticket
class ModelTicketModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):
    pass



class ModelTicketModelInheritedCases(
    ModelTicketModelTestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketModelPyTest(
    ModelTicketModelTestCases,
):
    pass
