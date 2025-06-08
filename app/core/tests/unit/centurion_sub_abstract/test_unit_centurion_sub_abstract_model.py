import pytest

from django.db import models

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


    def test_method_get_url_attribute__is_submodel_set(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        model_instance.id = 1

        model_instance.model = model_instance

        url_basename = f'v2:_api_{model_instance._meta.model_name}_sub-detail'

        url = model_instance.get_url( relative = True)

        reverse.assert_called_with(
            url_basename,
            None,
            {
                'app_label': model_instance._meta.app_label,
                'model_name': model_instance._meta.model_name,
                'model_id': model_instance.model.id,
                'pk': model_instance.id,
            },
            None,
            None
        )



    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        model_instance.id = 1
        model_instance.model = model_instance

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'app_label': model_instance._meta.app_label,
            'model_name': model_instance._meta.model_name,
            'model_id': model_instance.model.id,
            'pk': model_instance.id,
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
            'page_layout': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
            'table_fields': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
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
