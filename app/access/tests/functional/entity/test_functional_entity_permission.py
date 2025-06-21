import pytest

from api.tests.functional.test_functional_api_permissions import (
    APIPermissionsInheritedCases,
)



class EntityPermissionsAPITestCases(
    APIPermissionsInheritedCases,
):

    add_data: dict = {}

    app_namespace = 'v2'

    change_data = {}

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_kwargs: dict = {}

    url_name = '_api_entity'

    url_view_kwargs: dict = {}



    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



class EntityPermissionsAPIInheritedCases(
    EntityPermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_name = '_api_entity_sub'


    @pytest.fixture(scope='class')
    def inherited_var_setup(self, request):

        request.cls.url_kwargs.update({
            'model_name': self.model._meta.sub_model_type
        })

        request.cls.url_view_kwargs.update({
            'model_name': self.model._meta.sub_model_type
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


class EntityPermissionsAPIPyTest(
    EntityPermissionsAPITestCases,
):

    pass
