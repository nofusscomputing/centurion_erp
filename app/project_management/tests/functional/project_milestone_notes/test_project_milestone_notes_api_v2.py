from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.model_notes_api_fields import ModelNotesNotesAPIFields

from project_management.models.projects import Project
from project_management.models.project_milestone_notes import ProjectMilestone, ProjectMilestoneNotes



class ProjectMilestoneNotesAPI(
    ModelNotesNotesAPIFields,
    TestCase,
):

    model = ProjectMilestoneNotes

    view_name: str = '_api_v2_project_milestone_note'

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
            model = ProjectMilestone.objects.create(
                organization = self.organization,
                name = 'note model',
                project = Project.objects.create(
                    organization = self.organization,
                    name = 'proj',
                )
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        self.url_view_kwargs = {
            'project_id': self.item.model.project.pk,
            'model_id': self.item.model.pk,
            'pk': self.item.pk
        }

        self.make_request()
