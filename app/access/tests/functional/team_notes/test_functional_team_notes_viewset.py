from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.viewsets.team_notes import ViewSet

from core.tests.abstract.test_functional_notes_viewset import (
    ModelNotesViewSetBase,
    ModelNotesMetadata,
    ModelNotesPermissionsAPI,
    ModelNotesSerializer
)



class ViewSetBase(
    ModelNotesViewSetBase
):

    viewset = ViewSet

    url_name = '_api_v2_team_note'

    @classmethod
    def setUpTestData(self):
        

        super().setUpTestData()

        self.item = self.viewset.model.objects.create(
            organization = self.organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.viewset.model.model.field.related_model.objects.create(
                organization = self.organization,
                name = 'note model'
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )

        self.other_org_item = self.viewset.model.objects.create(
            organization = self.different_organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.viewset.model.model.field.related_model.objects.create(
                organization = self.different_organization,
                name = 'note model'
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
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
                name = 'note model global_organization'
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )

        self.url_kwargs = {
            'organization_id': self.organization.id,
            'model_id': self.item.model.pk,
        }

        self.url_view_kwargs = {
            'organization_id': self.organization.id,
            'model_id': self.item.model.pk,
            'pk': self.item.id
        }



class TeamModelNotesPermissionsAPI(
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





class TeamModelNotesSerializer(
    ViewSetBase,
    ModelNotesSerializer,
    TestCase,
):

    pass



class TeamModelNotesMetadata(
    ViewSetBase,
    ModelNotesMetadata,
    TestCase,

):

    pass
