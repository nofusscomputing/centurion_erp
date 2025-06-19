import pytest

from access.tests.functional.entity.test_functional_entity_permission import (
    EntityPermissionsAPIInheritedCases
)



class PersonPermissionsAPITestCases(
    EntityPermissionsAPIInheritedCases,
):

    add_data: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Strange',
        'dob': '2025-04-08',
    }

    # app_namespace = 'v2'

    # change_data = {}

    # delete_data = {}

    kwargs_create_item: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Weird',
        'dob': '2025-04-08',
    }

    kwargs_create_item_diff_org: dict = {
        'f_name': 'Ian',
        'm_name': 'Peter',
        'l_name': 'Funny',
        'dob': '2025-04-08',
    }

    # url_kwargs: dict = {}

    # url_name = '_api_entity'

    # url_view_kwargs: dict = {}



class PersonPermissionsAPIInheritedCases(
    PersonPermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    # url_name = '_api_entity_sub'


    # @pytest.fixture(scope='class')
    # def inherited_var_setup(self, request):

    #     request.cls.url_kwargs.update({
    #         'entity_model': self.model._meta.sub_model_type
    #     })

    #     request.cls.url_view_kwargs.update({
    #         'entity_model': self.model._meta.sub_model_type
    #     })



    # @pytest.fixture(scope='class', autouse = True)
    # def class_setup(self, request, django_db_blocker,
    #     model,
    #     var_setup,
    #     prepare,
    #     inherited_var_setup,
    #     diff_org_model,
    #     create_model,
    # ):

    #     pass


class PersonPermissionsAPIPyTest(
    PersonPermissionsAPITestCases,
):

    pass
