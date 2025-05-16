from django.test import TestCase

from access.models.tenant import Tenant as Organization

from centurion.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from devops.models.feature_flag import FeatureFlag

from itam.models.software import Software



class Model(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = FeatureFlag


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        self.organization = Organization.objects.create(name='test_org')


        self.kwargs_item_create = {
            'name': 'one',
            'software': Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            'description': 'desc',
            'enabled': True
        }

        super().setUpTestData()



    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert type(self.model.app_namespace) is str


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace == 'devops'
