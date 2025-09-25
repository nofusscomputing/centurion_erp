import pytest

from core.tests.unit.model_tickets.test_unit_model_tickets_model import (
    ModelTicketModelInheritedCases
)



@pytest.mark.model_modelticketmetamodel
class ModelTicketMetaModelTestCases(
    ModelTicketModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



class ModelTicketMetaModelInheritedCases(
    ModelTicketMetaModelTestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketMetaModelPyTest(
    ModelTicketMetaModelTestCases,
):
    pass
