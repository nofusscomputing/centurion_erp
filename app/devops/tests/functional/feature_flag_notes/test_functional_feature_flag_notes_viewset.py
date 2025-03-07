from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.viewsets.feature_flag_notes import ViewSet

from core.tests.abstract.test_functional_notes_viewset import (
    ModelNotesViewSetBase,
    ModelNotesMetadata,
    ModelNotesPermissionsAPI,
    ModelNotesSerializer
)

from itam.models.software import Software



class ViewSetBase(
    ModelNotesViewSetBase
):

    viewset = ViewSet

    url_name = 'devops:_api_v2_feature_flag_note'

    @classmethod
    def setUpTestData(self):
        

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

        self.item = self.viewset.model.objects.create(
            organization = self.organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.viewset.model.model.field.related_model.objects.create(
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

        software = Software.objects.create(
            organization = self.organization,
            name = 'two',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.other_org_item = self.viewset.model.objects.create(
            organization = self.different_organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.viewset.model.model.field.related_model.objects.create(
                organization = self.organization,
                name = 'two',
                software = software,
                description = 'desc',
                model_notes = 'text',
                enabled = True
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        SoftwareEnableFeatureFlag.objects.create(
            organization = self.global_organization,
            software = software,
            enabled = True
        )

        self.global_org_item = self.viewset.model.objects.create(
            organization = self.global_organization,
            content = 'a random comment global_organization',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.viewset.model.model.field.related_model.objects.create(
                organization = self.global_organization,
                name = 'note model global_organization',
                software = software,
                description = 'desc',
                model_notes = 'text',
                enabled = True
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )

        self.url_kwargs = {
            'model_id': self.item.model.pk,
        }

        self.url_view_kwargs = {
            'model_id': self.item.model.pk,
            'pk': self.item.id
        }



class ManufacturerModelNotesPermissionsAPI(
    ViewSetBase,
    ModelNotesPermissionsAPI,
    TestCase,
):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a global model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass





class ManufacturerBaseModelNotesSerializer(
    ViewSetBase,
    ModelNotesSerializer,
    TestCase,
):

    pass



class ManufacturerModelNotesMetadata(
    ViewSetBase,
    ModelNotesMetadata,
    TestCase,

):

    pass
