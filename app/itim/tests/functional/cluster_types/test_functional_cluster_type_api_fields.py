import pytest

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_clustertype
class ClusterTypeAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'config': {
                'expected': dict
            },
            'config.config_key_1': {
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
