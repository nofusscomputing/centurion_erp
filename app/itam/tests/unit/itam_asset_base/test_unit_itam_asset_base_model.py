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



class ITAMAssetModelInheritedCases(
    ITAMAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAMAssetModelPyTest(
    ITAMAssetModelTestCases,
):
    pass
