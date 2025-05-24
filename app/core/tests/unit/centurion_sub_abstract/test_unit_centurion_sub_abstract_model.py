import pytest

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelTestCases,
    CenturionAbstractModelInheritedCases,
)



@pytest.mark.models
@pytest.mark.unit
class CenturionSubAbstractModelTestCases(
    CenturionAbstractModelTestCases
):


    parameterized_class_attributes = {
        '_is_submodel': {
            'value': True,
        }
    }




class CenturionSubAbstractModelInheritedCases(
    CenturionSubAbstractModelTestCases,
    CenturionAbstractModelInheritedCases,
):

    pass



class CenturionSubAbstractModelPyTest(
    CenturionSubAbstractModelTestCases,
):

    def test_model_is_abstract(self, model):

        assert model._meta.abstract
