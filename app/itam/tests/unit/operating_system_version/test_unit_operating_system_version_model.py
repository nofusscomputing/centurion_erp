from django.test import TestCase

from access.models.tenant import Tenant as Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)


from itam.models.operating_system import OperatingSystem, OperatingSystemVersion



class OperatingSystemVersionModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = OperatingSystemVersion


    @classmethod
    def setUpTestData(self):
        """ Setup Test

        """

        self.organization = Organization.objects.create(name='test_org')


        self.parent_item = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'os_name'
        )

        self.kwargs_item_create = {
            'name': "12",
            'operating_system': self.parent_item,
        }

        super().setUpTestData()
