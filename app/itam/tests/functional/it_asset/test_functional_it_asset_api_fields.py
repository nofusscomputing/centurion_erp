import pytest

from rest_framework.relations import Hyperlink

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_api_fields import (
    ITAMAssetBaseAPIInheritedCases
)



@pytest.mark.model_itasset
class ITAssetAPITestCases(
    ITAMAssetBaseAPIInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'uuid': {
                'expected': str
            },
            'imei': {
                'expected': str
            },
            'mac_address': {
                'expected': str
            },
            'puk': {
                'expected': str
            },
            'puk_pin': {
                'expected': str
            },
            'device_model': {
                'expected': dict
            },
            'device_model.id': {
                'expected': int
            },
            'device_model.display_name': {
                'expected': str
            },
            'device_model.url': {
                'expected': Hyperlink
            },
            'config': {
                'expected': dict
            },
            'inventorydate': {
                'expected': str
            },
            'is_virtual': {
                'expected': bool
            },
            'asset_type': {
                'expected': dict
            },
            'asset_type.id': {
                'expected': int
            },
            'asset_type.display_name': {
                'expected': str
            },
            'asset_type.url': {
                'expected': Hyperlink
            },
        }



class ITAssetAPIInheritedCases(
    ITAssetAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetAPIPyTest(
    ITAssetAPITestCases,
):

    pass
