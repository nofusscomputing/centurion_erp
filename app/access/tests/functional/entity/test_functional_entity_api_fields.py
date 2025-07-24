import pytest

from access.models.entity import Entity

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_entity
class EntityAPITestCases(
    APIFieldsInheritedCases,
):

    base_model = Entity


    @property
    def parameterized_api_fields(self):

        return {
            'entity_type': {
                'expected': str
            },
            '_urls.history': {
                'expected': str
            },
            '_urls.knowledge_base': {
                'expected': str
            }
        }



class EntityAPIInheritedCases(
    EntityAPITestCases,
):
    pass



@pytest.mark.module_access
class EntityAPIPyTest(
    EntityAPITestCases,
):

    pass
