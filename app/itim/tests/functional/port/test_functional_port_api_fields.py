import pytest

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_port
class ClusterTypeAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'number': {
                'expected': int
            },
            'description': {
                'expected': str
            },
            'protocol': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class ClusterTypeAPIInheritedCases(
    ClusterTypeAPITestCases,
):
    pass



@pytest.mark.module_itim
class ClusterTypeAPIPyTest(
    ClusterTypeAPITestCases,
):

    pass
