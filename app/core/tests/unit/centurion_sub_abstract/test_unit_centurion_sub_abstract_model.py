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

    @property
    def parameterized_class_attributes(self):
        
        return {
            'model_tag': {
                'type': type(None),
                'value': None,
            },
            'url_model_name': {
                'type': type(None),
                'value': None,
            }
        }


    @pytest.mark.xfail( reason = 'This model is an abstract model')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_model_is_abstract(self, model):

        assert model._meta.abstract
