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


    @pytest.fixture( scope = 'class')
    def setup_model(self, request,
        model,
    ):

        if model != self.base_model:

            request.cls.url_view_kwargs.update({
                'asset_model': model._meta.sub_model_type,
            })


    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_pre,
        setup_model,
        create_model,
        setup_post,
    ):

        pass


    parameterized_test_data = {
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

    kwargs_create_item: dict = {
        'asset_number': '123123',
        'serial_number': '65756756756',
    }

    url_ns_name = 'accounting:_api_asset'
    """Url namespace (optional, if not required) and url name"""



class AssetBaseAPIInheritedCases(
    AssetBaseAPITestCases,
):

    kwargs_create_item: dict = None

    model = None

    url_ns_name = 'accounting:_api_asset_sub'



@pytest.mark.module_accounting
class AssetBaseAPIPyTest(
    AssetBaseAPITestCases,
):

    pass
