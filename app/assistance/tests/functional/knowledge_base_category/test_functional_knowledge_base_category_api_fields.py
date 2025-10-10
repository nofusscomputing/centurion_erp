import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_knowledgebasecategory
class knowledgeBaseCategoryAPITestCases(
    APIFieldsInheritedCases,
):

    @pytest.fixture( scope = 'class')
    def second_model(self, request, django_db_blocker,
        model, model_kwargs, model_group, kwargs_group
    ):

        item = None

        with django_db_blocker.unblock():

            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in model_kwargs().items():

                field = model._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })


            # Switch model fields so all fields can be checked
            group = model_group.objects.create( **kwargs_group() )
            kwargs_many_to_many.update({ 'target_team': [ group ]})
            del kwargs['target_user']

            kwargs['parent_category'] = request.cls.item


            item_two = model.objects.create(
                **kwargs
            )


            for key, value in kwargs_many_to_many.items():

                field = getattr(item_two, key)

                for entry in value:

                    field.add(entry)


            request.cls.item_two = item_two

        yield item_two

        with django_db_blocker.unblock():

            item_two.delete()

            group.delete()

            del request.cls.item_two


    @pytest.fixture( scope = 'class', autouse = True)
    def class_setup(self,
        create_model,
        second_model,
        make_request,
    ):

        pass

    @property
    def parameterized_api_fields(self):

        return {
            'parent_category': {
                'expected': dict
            },
            'parent_category.id': {
                'expected': int
            },
            'parent_category.display_name': {
                'expected': str
            },
            'parent_category.url': {
                'expected': str
            },
            'name': {
                'expected': str
            },
            'target_team': {
                'expected': list
            },
            'target_team.0.id': {
                'expected': int
            },
            'target_team.0.display_name': {
                'expected': str
            },
            'target_team.0.url': {
                'expected': str
            },
            'target_user': {
                'expected': dict
            },
            'target_user.id': {
                'expected': int
            },
            'target_user.display_name': {
                'expected': str
            },
            'target_user.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class knowledgeBaseCategoryAPIInheritedCases(
    knowledgeBaseCategoryAPITestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgeBaseCategoryAPIPyTest(
    knowledgeBaseCategoryAPITestCases,
):

    pass
