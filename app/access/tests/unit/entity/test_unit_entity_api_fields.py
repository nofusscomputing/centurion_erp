import pytest

from access.models.entity import Entity

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



class EntityAPITestCases(
    APIFieldsInheritedCases,
):

    base_model = Entity


    @pytest.fixture( scope = 'class')
    def setup_model(self, request,
        model,
    ):

        if model != self.base_model:
        
            request.cls.url_view_kwargs.update({
                'entity_model': model._meta.sub_model_type,
            })


    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        setup_pre,
        setup_model,
        create_model,
        setup_post,
    ):

        pass


    parameterized_test_data = {
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

    kwargs_create_item: dict = {
        'entity_type': 'entity',
    }

    url_ns_name = '_api_v2_entity'
    """Url namespace (optional, if not required) and url name"""



class EntityAPIInheritedCases(
    EntityAPITestCases,
):

    kwargs_create_item: dict = None

    model = None

    url_ns_name = '_api_v2_entity_sub'



class EntityAPIPyTest(
    EntityAPITestCases,
):

    pass
