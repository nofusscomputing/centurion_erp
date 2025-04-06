from django.test import TestCase

from access.models.role import Role
from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel



class ModelTestCases(
    TenancyModel,
):

    model = None

    kwargs_item_create: dict = None

    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        different_organization = Organization.objects.create(name='test_different_organization')

        self.item = self.model.objects.create(
            organization = self.organization,
            model_notes = 'notes',
            **self.kwargs_item_create,
        )



class RoleModelTest(
    ModelTestCases,
    TestCase,
):

    model = Role

    kwargs_item_create: dict = {
        'name': 'a role'
    }
