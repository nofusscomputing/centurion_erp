import pytest

from core.tests.unit.model_tickets.test_unit_model_tickets_model import (
    ModelTicketModelInheritedCases
)



@pytest.mark.tickets
@pytest.mark.model_modelticketmeta
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


    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Base model does not contain a model field.' )
    def test_field_content_type_correct(self, model_instance, model_modelticket ):
        """Test model field

        Ensure that the model in field `content_type` is an actual model and
        not a `<model name>Ticket`.
        """

        assert not issubclass(model_instance.content_type.model_class(), model_modelticket)



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'Base model does not contain a model field.' )
    def test_method_value___str___has_model(self, model_instance ):
        """Test Method

        Ensure method `__str__` contains the model_tag for the model in
        question.
        """

        assert model_instance.content_type.model_class().model_tag is not None, \
            'The model must have a defined tag for this test to function correctly.'

        assert f"${model_instance.content_type.model_class().model_tag}" in model_instance.__str__()

