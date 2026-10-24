import pytest

from django.db import models

from accounting.tests.unit.asset_base.test_unit_asset_base_model import (
    AssetBaseModelInheritedCases,
    AssetBase
)

from itam.models.itam_asset_base import ITAMAssetBase



@pytest.mark.model_itamassetbase
class ITAMAssetModelTestCases(
    AssetBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            'app_namespace': {
                'type': str,
                'value': 'accounting'
            },
            'model_tag': {
                'type': str,
                'value': 'asset'
            },
            'url_model_name': {
                'type': str,
                'value': 'asset'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}


    def test_class_inherits_itamassetbase(self, model):
        """ Class inheritence

        Model Must Inherit from itamassetbase
        """

        assert issubclass(model, ITAMAssetBase)



    def test_function__str__has_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if asset_number exists that it is used in model
        stringify.
        """

        test_model = model( **model_kwargs() )

        assert str(test_model).endswith(test_model.asset_number)



    def test_function__str__no_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if there is not asset_number that it is not used in model
        stringify.
        """

        kwargs = model_kwargs()
        del kwargs['asset_number']

        test_model = model( **kwargs )

        assert test_model._meta.verbose_name == str(test_model)



class ITAMAssetModelInheritedCases(
    ITAMAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAMAssetModelPyTest(
    ITAMAssetModelTestCases,
):
    pass
