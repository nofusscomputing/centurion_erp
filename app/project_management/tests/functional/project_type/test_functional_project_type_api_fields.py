import pytest

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_projecttype
class ProjectTypeAPITestCases(
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
            'modified': {
                'expected': str
            }
        }



class ProjectTypeAPIInheritedCases(
    ProjectTypeAPITestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTypeAPIPyTest(
    ProjectTypeAPITestCases,
):

    pass
