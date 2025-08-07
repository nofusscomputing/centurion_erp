import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_featureflag
class FeatureFlagAPITestCases(
    APIFieldsInheritedCases,
):

    # @pytest.fixture( scope = 'class')
    # def second_model(self, request, django_db_blocker,
    #     model, model_kwargs
    # ):

    #     item = None

    #     with django_db_blocker.unblock():

    #         kwargs_many_to_many = {}

    #         kwargs = {}

    #         for key, value in model_kwargs.items():

    #             field = model._meta.get_field(key)

    #             if isinstance(field, models.ManyToManyField):

    #                 kwargs_many_to_many.update({
    #                     key: value
    #                 })

    #             else:

    #                 kwargs.update({
    #                     key: value
    #                 })


    #         # Switch model fields so all fields can be checked
    #         kwargs_many_to_many.update({ 'responsible_teams': kwargs_many_to_many['target_team']})
    #         del kwargs_many_to_many['target_team']

    #         kwargs.update({ 'target_user': kwargs['responsible_user']})
    #         del kwargs['responsible_user']


    #         item_two = model.objects.create(
    #             **kwargs
    #         )


    #         for key, value in kwargs_many_to_many.items():

    #             field = getattr(item_two, key)

    #             for entry in value:

    #                 field.add(entry)


    #         request.cls.item_two = item_two

    #     yield item_two

    #     with django_db_blocker.unblock():

    #         item_two.delete()

    #         del request.cls.item_two


    # @pytest.fixture( scope = 'class', autouse = True)
    # def class_setup(self,
    #     create_model,
    #     second_model,
    #     make_request,
    # ):

    #     pass

    @property
    def parameterized_api_fields(self):

        return {
            'software': {
                'expected': dict
            },
            'software.id': {
                'expected': int
            },
            'software.display_name': {
                'expected': str
            },
            'software.url': {
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'description': {
                'expected': str
            },
            'enabled': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class FeatureFlagAPIInheritedCases(
    FeatureFlagAPITestCases,
):
    pass



@pytest.mark.module_assistance
class FeatureFlagAPIPyTest(
    FeatureFlagAPITestCases,
):

    pass
