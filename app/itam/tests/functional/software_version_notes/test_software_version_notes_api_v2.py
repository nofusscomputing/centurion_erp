from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.model_notes_api_fields import ModelNotesNotesAPIFields

from itam.models.software import Software
from itam.models.software_version_notes import SoftwareVersion, SoftwareVersionNotes



class SoftwareVersionNotesAPI(
    ModelNotesNotesAPIFields,
    TestCase,
):

    model = SoftwareVersionNotes

    view_name: str = '_api_v2_software_version_note'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Call parent setup
        2. Create a model note
        3. add url kwargs
        4. make the API request

        """

        super().setUpTestData()


        self.item = self.model.objects.create(
            organization = self.organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = SoftwareVersion.objects.create(
                organization = self.organization,
                name = '11',
                software = Software.objects.create(
                    organization = self.organization,
                    name = 'soft name'
                )
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        self.url_view_kwargs = {
            'software_id': self.item.model.software.pk,
            'model_id': self.item.model.pk,
            'pk': self.item.pk
        }

        self.make_request()
