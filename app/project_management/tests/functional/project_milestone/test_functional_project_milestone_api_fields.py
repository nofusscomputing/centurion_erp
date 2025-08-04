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

    # @pytest.fixture( scope = 'class')
    # def second_model(self, request, django_db_blocker,
    #     model, model_kwargs,
    #     model_team, kwargs_team
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


    #         # # Switch model fields so all fields can be checked
    #         # kwargs_many_to_many.update({ 'devices': kwargs_many_to_many['nodes']})
    #         # del kwargs_many_to_many['nodes']
    #         # # del kwargs_many_to_many['target_team']

    #         # kwargs.update({ 'parent_projectmilestone': self.item})
    #         del kwargs['manager_user']
    #         manager_team = model_team.objects.create( **kwargs_team )
    #         kwargs['manager_team'] = manager_team
    #         kwargs['external_ref'] = 1
    #         kwargs['external_system'] = 1

    #         kwargs['name'] = 'pro two'
    #         del kwargs['code']


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
    #         manager_team.delete()

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
            'model_notes': {
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
