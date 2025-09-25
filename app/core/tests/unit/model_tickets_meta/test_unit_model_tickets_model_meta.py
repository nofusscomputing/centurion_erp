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

    def test_method_get_url_kwargs(self, mocker, model, model_instance, settings):

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        assert model_instance.get_url_kwargs() == {
            'app_label': model_instance.model._meta.app_label,
            'model_name': model_instance.model._meta.model_name,
            'model_id': model_instance.model.pk,
            'pk': model_instance.id 
        }




@pytest.mark.module_core
class ModelTicketMetaModelPyTest(
    ModelTicketMetaModelTestCases,
):
    pass
