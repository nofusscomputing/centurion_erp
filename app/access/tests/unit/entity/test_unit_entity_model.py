from django.test import TestCase

from access.models.entity import Entity
from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel



class ModelTestCases(
    TenancyModel,
):

    model = Entity

    kwargs_item_create: dict = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        different_organization = Organization.objects.create(name='test_different_organization')

        self.item = self.model.objects.create(
            organization = self.organization,
            model_notes = 'notes',
            entity_type = self.model._meta.model_name,
            **self.kwargs_item_create,
        )



class EntityModelInheritedCases(
    ModelTestCases,
):
    """Sub-Entity Test Cases

    Test Cases for Entity models that inherit from model Entity
    """

    kwargs_item_create: dict = None

    model = None


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update(
            super().kwargs_item_create
        )

        super().setUpTestData()



class EntityModelTest(
    ModelTestCases,
    TestCase,
):

    pass
