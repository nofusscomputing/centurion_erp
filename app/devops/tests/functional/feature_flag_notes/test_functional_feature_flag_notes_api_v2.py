from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.model_notes_api_fields import ModelNotesNotesAPIFields

from devops.models.feature_flag_notes import FeatureFlag, FeatureFlagNotes
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software



class NotesAPI(
    ModelNotesNotesAPIFields,
    TestCase,
):

    model = FeatureFlagNotes

    view_name: str = 'devops:_api_v2_feature_flag_note'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Call parent setup
        2. Create a model note
        3. add url kwargs
        4. make the API request

        """

        super().setUpTestData()

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = FeatureFlag.objects.create(
                organization = self.organization,
                name = 'one',
                software = software,
                description = 'desc',
                model_notes = 'text',
                enabled = True
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        self.url_view_kwargs = {
            'model_id': self.item.model.pk,
            'pk': self.item.pk
        }

        self.make_request()
