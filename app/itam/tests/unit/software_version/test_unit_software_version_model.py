from django.test import TestCase

from access.models.organization import Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from itam.models.software import Software, SoftwareVersion



class SoftwareVersionModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = SoftwareVersion


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

        self.software = Software.objects.create(
            organization = self.organization,
            name = 'deviceone'
        )

        self.kwargs_item_create = {
            'name': '12',
            'software': self.software
        }

        super().setUpTestData()
