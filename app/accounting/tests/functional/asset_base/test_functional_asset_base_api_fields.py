import pytest

from accounting.models.asset_base import AssetBase

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_assetbase
class AssetBaseAPITestCases(
    APIFieldsInheritedCases,
):

    base_model = AssetBase


    @property
    def parameterized_api_fields(self):

        return {
            'asset_number': {
                'expected': str
            },
            'serial_number': {
                'expected': str
            },
            'asset_type': {
                'expected': str
            }
        }



class AssetBaseAPIInheritedCases(
    AssetBaseAPITestCases,
):

    pass



@pytest.mark.module_accounting
class AssetBaseAPIPyTest(
    AssetBaseAPITestCases,
):

    pass
