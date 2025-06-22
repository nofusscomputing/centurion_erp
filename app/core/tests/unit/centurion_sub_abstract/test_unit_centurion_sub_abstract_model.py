import pytest

from django.db import models

from centurion.tests.unit_models import ModelTestCases


@pytest.mark.models
@pytest.mark.unit
class CenturionSubAbstractModelTestCases(
    ModelTestCases
):


    @property
    def parameterized_class_attributes(self):

        return {
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


        model_instance.model = model_instance

        app_namespace = ''
        if model_instance.app_namespace:
            app_namespace = model_instance.app_namespace + ':'

        url_model_name = model_instance._meta.model_name
        if model_instance.url_model_name:
            url_model_name = model_instance.url_model_name

        url_basename = f'v2:{app_namespace}_api_{url_model_name}_sub-detail'

        url = model_instance.get_url( relative = True)

        reverse.assert_called_with(
            url_basename,
            None,
            {
                # 'app_label': model_instance._meta.app_label,
                'model_name': model_instance._meta.model_name,
                # 'model_id': model_instance.model.id,
                'pk': model_instance.id,
            },
            None,
            None
        )



    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        model_instance.model = model_instance

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            # 'app_label': model_instance._meta.app_label,
            'model_name': model_instance._meta.model_name,
            # 'model_id': model_instance.model.id,
            'pk': model_instance.id,
        }






class CenturionSubAbstractModelInheritedCases(
    CenturionSubAbstractModelTestCases,
):

    pass
