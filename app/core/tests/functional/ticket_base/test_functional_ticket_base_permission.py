import pytest

from api.tests.functional.test_functional_api_permissions import (
    APIPermissionsInheritedCases,
)



@pytest.mark.model_ticketbase
class PermissionsAPITestCases(
    APIPermissionsInheritedCases,
):

    add_data: dict = {
        'title': 'ticket one',
        'description': 'sadsa'
    }

    app_namespace = 'v2'

    change_data = {'description': 'device'}

    delete_data = {}

    kwargs_create_item: dict = {
        'title': 'ticket two',
        'description': 'sadsa'
    }

    kwargs_create_item_diff_org: dict = {
        'title': 'ticket three',
        'description': 'sadsa'
    }

    url_kwargs: dict = {}

    url_name = '_api_v2_ticket'

    url_view_kwargs: dict = {}




    @pytest.fixture(scope='class')
    def opened_by_var_setup(self, request):

        request.cls.kwargs_create_item.update({
            'opened_by': request.cls.view_user
        })

        request.cls.kwargs_create_item_diff_org.update({
            'opened_by': request.cls.view_user
        })

        if request.cls.add_data is not None:

            request.cls.add_data.update({
                'opened_by': request.cls.view_user.pk
            })



    @pytest.fixture(scope='class', autouse = True)
    def class_setup(self, request, django_db_blocker,
        model,
        var_setup,
        prepare,
        opened_by_var_setup,
        diff_org_model,
        create_model,
        post_model
    ):

        pass



    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



class TicketBasePermissionsAPIInheritedCases(
    PermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None


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
        opened_by_var_setup,
        inherited_var_setup,
        diff_org_model,
        create_model,
    ):

        pass

@pytest.mark.module_core
class TicketBasePermissionsAPIPyTest(
    PermissionsAPITestCases,
):

    pass
