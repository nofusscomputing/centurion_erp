import pytest

from rest_framework.relations import Hyperlink


from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_itassetmodel
class ITAssetModelAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'device_type': {
                'expected': dict
            },
            'device_type.id': {
                'expected': int
            },
            'device_type.display_name': {
                'expected': str
            },
            'device_type.url': {
                'expected': Hyperlink
            },
            'manufacturer': {
                'expected': dict
            },
            'manufacturer.id': {
                'expected': int
            },
            'manufacturer.display_name': {
                'expected': str
            },
            'manufacturer.url': {
                'expected': str
            },


            'imei': {
                'expected': bool
            },
            'mac_address': {
                'expected': bool
            },
            'puk': {
                'expected': bool
            },
            'puk_pin': {
                'expected': bool
            },
            'serial_number': {
                'expected': bool
            },
        }



class ITAssetModelAPIInheritedCases(
    ITAssetModelAPITestCases,
):

    pass



@pytest.mark.module_itam
class ITAssetModelAPIPyTest(
    ITAssetModelAPITestCases,
):

    pass
