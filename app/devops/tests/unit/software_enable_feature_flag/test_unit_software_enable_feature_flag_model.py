from django.test import TestCase

from access.models.tenant import Tenant as Organization
 
from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



class Model(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = SoftwareEnableFeatureFlag

    should_model_history_be_saved: bool = False

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
            'organization': self.organization,
            'software': Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            'enabled': True
        }

        super().setUpTestData()
