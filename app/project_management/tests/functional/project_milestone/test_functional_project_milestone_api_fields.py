import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_projectmilestone
class ProjectMilestoneAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.markdown': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.render': {
                'expected': models.NOT_PROVIDED
            },
            'name': {
                'expected': str
            },
            'start_date': {
                'expected': str
            },
            'finish_date': {
                'expected': str
            },
            'project': {
                'expected': dict
            },
            'project.id': {
                'expected': int
            },
            'project.display_name': {
                'expected': str
            },
            'project.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class ProjectMilestoneAPIInheritedCases(
    ProjectMilestoneAPITestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectMilestoneAPIPyTest(
    ProjectMilestoneAPITestCases,
):

    pass
