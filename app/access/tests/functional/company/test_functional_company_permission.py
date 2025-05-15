import pytest

from access.tests.functional.entity.test_functional_entity_permission import (
    EntityPermissionsAPIInheritedCases
)



class CompanyPermissionsAPITestCases(
    EntityPermissionsAPIInheritedCases,
):

    add_data: dict = {
        'name': 'Ian1',
    }

    kwargs_create_item: dict = {
        'name': 'Ian2',
    }

    kwargs_create_item_diff_org: dict = {
        'name': 'Ian3',
    }



class CompanyPermissionsAPIInheritedCases(
    CompanyPermissionsAPITestCases,
):

    add_data: dict = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None



class CompanyPermissionsAPIPyTest(
    CompanyPermissionsAPITestCases,
):

    pass
