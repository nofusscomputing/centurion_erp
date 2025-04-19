from django.contrib.auth.models import  User
from django.contrib.contenttypes.models import ContentType

from access.models.organization import Organization

from app.tests.unit.test_unit_models import TenancyObjectInheritedCases

from core.models.model_notes import ModelNotes



class ModelNotesTestCases(
    TenancyObjectInheritedCases
):

    model = ModelNotes



class ModelNotesInheritedCases(
    ModelNotesTestCases
):

    kwargs_item_create = None


    model = None


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

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



        self.user = User.objects.create_user(username="test_user_view", password="password")

        self.kwargs_item_create = {
            'content': 'a random comment for an exiting item',
            'content_type': ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            'model': self.model.model.field.related_model.objects.create(
                **self.kwargs_create_related_model,
            ),
            'created_by': self.user,
        }

        super().setUpTestData()



class ModelNotesTest(
    ModelNotesTestCases
):

    pass
