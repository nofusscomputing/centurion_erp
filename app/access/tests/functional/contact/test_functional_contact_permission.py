import pytest

from access.tests.functional.person.test_functional_person_permission import (
    PersonPermissionsAPIInheritedCases
)



class ContactPermissionsAPITestCases(
    PersonPermissionsAPIInheritedCases,
):

    add_data: dict = {
        'email': 'ipfunny@unit.test',
    }

    kwargs_create_item: dict = {
        'email': 'ipweird@unit.test',
    }

    kwargs_create_item_diff_org: dict = {
        'email': 'ipstrange@unit.test',
    }



class ContactPermissionsAPIInheritedCases(
    ContactPermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    # url_name = '_api_entity_sub'


    # @pytest.fixture(scope='class')
    # def inherited_var_setup(self, request):

    #     request.cls.url_kwargs.update({
    #         'model_name': self.model._meta.sub_model_type
    #     })

    #     request.cls.url_view_kwargs.update({
    #         'model_name': self.model._meta.sub_model_type
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


class ContactPermissionsAPIPyTest(
    ContactPermissionsAPITestCases,
):

    pass
