import pytest

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_projectmilestone
class ProjectStateAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'runbook': {
                'expected': dict
            },
            'runbook.id': {
                'expected': int
            },
            'runbook.display_name': {
                'expected': str
            },
            'runbook.url': {
                'expected': str
            },
            'is_completed': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class ProjectStateAPIInheritedCases(
    ProjectStateAPITestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectStateAPIPyTest(
    ProjectStateAPITestCases,
):

    pass
