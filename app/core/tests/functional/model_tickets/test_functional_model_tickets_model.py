import pytest

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)


@pytest.mark.tickets
@pytest.mark.model_modelticket
class ModelTicketModelTestCases(
    CenturionAbstractModelInheritedCases
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
