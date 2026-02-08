import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_project
class ProjectAPITestCases(
    APIFieldsInheritedCases,
):

    @pytest.fixture( scope = 'class')
    def second_model(self, request, django_db_blocker,
        model, model_kwargs,
        model_group, kwargs_group
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


            # # Switch model fields so all fields can be checked
            # kwargs_many_to_many.update({ 'devices': kwargs_many_to_many['nodes']})
            # del kwargs_many_to_many['nodes']
            # # del kwargs_many_to_many['target_team']

            # kwargs.update({ 'parent_project': self.item})
            del kwargs['manager_user']
            manager_team = model_group.objects.create( **kwargs_group() )
            kwargs['manager_team'] = manager_team
            kwargs['external_ref'] = 1
            kwargs['external_system'] = 1

            kwargs['name'] = 'pro two'
            del kwargs['code']


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
            manager_team.delete()

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
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.markdown': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.render': {
                'expected': models.NOT_PROVIDED
            },
            'external_ref': {
                'expected': int
            },
            'external_system': {
                'expected': int
            },
            'name': {
                'expected': str
            },
            'description': {
                'expected': dict
            },
            'description.markdown': {
                'expected': str
            },
            'description.render': {
                'expected': dict
            },
            'priority': {
                'expected': int
            },
            'state': {
                'expected': dict
            },
            'state.id': {
                'expected': int
            },
            'state.display_name': {
                'expected': str
            },
            'state.url': {
                'expected': Hyperlink
            },
            'project_type': {
                'expected': dict
            },
            'project_type.id': {
                'expected': int
            },
            'project_type.display_name': {
                'expected': str
            },
            'project_type.url': {
                'expected': Hyperlink
            },
            'code': {
                'expected': str
            },
            'planned_start_date': {
                'expected': str
            },
            'planned_finish_date': {
                'expected': str
            },
            'real_finish_date': {
                'expected': str
            },
            'manager_user': {
                'expected': dict
            },
            'manager_user.id': {
                'expected': int
            },
            'manager_user.display_name': {
                'expected': str
            },
            'manager_user.url': {
                'expected': Hyperlink
            },
            'manager_team': {
                'expected': dict
            },
            'manager_team.id': {
                'expected': int
            },
            'manager_team.display_name': {
                'expected': str
            },
            'manager_team.url': {
                'expected': Hyperlink
            },
            'team_members': {
                'expected': list
            },
            'team_members.0.id': {
                'expected': int
            },
            'team_members.0.display_name': {
                'expected': str
            },
            'team_members.0.url': {
                'expected': Hyperlink
            },
            'is_deleted': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class ProjectAPIInheritedCases(
    ProjectAPITestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectAPIPyTest(
    ProjectAPITestCases,
):

    pass
