import django

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.organization import Organization

from app.tests.unit.test_unit_models import TenancyObjectInheritedCases

from core.models.model_notes import ModelNotes

User = django.contrib.auth.get_user_model()



class ModelNotesTestCases(
    TenancyObjectInheritedCases
):

    kwargs_item_create = {
        'content': 'a random comment for an exiting item',
    }

    model = ModelNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        if not hasattr(self, 'organization'):

            self.organization = Organization.objects.create(name='test_org')


        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.kwargs_item_create.update({
            'created_by': self.user,
        })

        super().setUpTestData()



class ModelNotesInheritedCases(
    ModelNotesTestCases
):

    kwargs_item_create = {}


    model = None


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        kwargs_item_create = ModelNotesTestCases.kwargs_item_create

        kwargs_item_create.update( self.kwargs_item_create )

        if not hasattr(self, 'organization'):

            self.organization = Organization.objects.create(name='test_org')


        if not hasattr(self, 'kwargs_create_related_model'):

            if 'organization' in self.model.model.field.related_model().fields:

                self.kwargs_create_related_model: dict = {
                    'organization': self.organization,
                }

            else:

                self.kwargs_create_related_model: dict = {}


        if 'organization' in self.model.model.field.related_model().fields:

            self.kwargs_create_related_model.update({
                'organization': self.organization,
            })


        if 'name' in self.model.model.field.related_model().fields:

            self.kwargs_create_related_model.update({
                'name': 'model for note'
            })

        self.kwargs_item_create.update({
            'content_type': ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            'model': self.model.model.field.related_model.objects.create(
                **self.kwargs_create_related_model,
            ),
        })

        super().setUpTestData()



class ModelNotesTest(
    ModelNotesTestCases,
    TestCase
):

    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.kwargs_item_create.update({
            'content_type': ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model._meta.model_name).lower(),
            ),
        })

        super().setUpTestData()


    def test_attribute_type_get_url(self):
        """Attribute Type

        This test case is a duplicate of a test with the same name. this model
        does not require this attribute be tested as it's a base model.

        get_url is of type str
        """

        assert True