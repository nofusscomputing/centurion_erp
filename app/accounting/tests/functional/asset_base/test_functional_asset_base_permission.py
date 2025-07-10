import pytest

from api.tests.functional.test_functional_api_permissions import (
    APIPermissionsInheritedCases,
)



@pytest.mark.model_assetbase
class PermissionsAPITestCases(
    APIPermissionsInheritedCases,
):

    add_data: dict = {
        'asset_number': 'abc',
        'serial_number': 'def',
        'model_notes': 'sdasds',
    }

    app_namespace = 'v2'

    change_data = {'asset_number': 'xyz'}

    delete_data = {}

    kwargs_create_item: dict = {
        'asset_number': 'ghi',
        'serial_number': 'jkl',
        'model_notes': 'sdasds',
    }

    kwargs_create_item_diff_org: dict = {
        'asset_number': 'mno',
        'serial_number': 'pqr',
        'model_notes': 'sdasds',
    }

    url_kwargs: dict = {}

    url_name = 'accounting:_api_v2_asset'

    url_view_kwargs: dict = {}



    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



class AssetBasePermissionsAPIInheritedCases(
    PermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_name = 'accounting:_api_v2_asset_sub'


    @pytest.fixture(scope='class')
    def inherited_var_setup(self, request):

        request.cls.url_kwargs.update({
            'asset_model': self.model._meta.sub_model_type
        })

        request.cls.url_view_kwargs.update({
            'asset_model': self.model._meta.sub_model_type
        })



    @pytest.fixture(scope='class', autouse = True)
    def class_setup(self, request, django_db_blocker,
        model,
        var_setup,
        prepare,
        inherited_var_setup,
        diff_org_model,
        create_model,
    ):

        pass



@pytest.mark.module_accounting
class AssetBasePermissionsAPIPyTest(
    PermissionsAPITestCases,
):

    pass
