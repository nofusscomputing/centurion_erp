import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_knowledgebase
class knowledgeBaseAPITestCases(
    APIFieldsInheritedCases,
):

    @pytest.fixture( scope = 'class')
    def second_model(self, request, django_db_blocker,
        model, model_kwargs
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
            kwargs_many_to_many.update({ 'responsible_teams': kwargs_many_to_many['target_team']})
            del kwargs_many_to_many['target_team']

            kwargs.update({ 'target_user': kwargs['responsible_user']})
            del kwargs['responsible_user']


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
            'title': {
                'expected': str
            },
            'summary': {
                'expected': dict
            },
            'summary.markdown': {
                'expected': str
            },
            'summary.render': {
                'expected': dict
            },
            'content': {
                'expected': dict
            },
            'content.markdown': {
                'expected': str
            },
            'content.render': {
                'expected': dict
            },
            'category': {
                'expected': dict
            },
            'category.id': {
                'expected': int
            },
            'category.display_name': {
                'expected': str
            },
            'category.url': {
                'expected': str
            },
            'release_date': {
                'expected': str
            },
            'expiry_date': {
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
            'responsible_user': {
                'expected': dict
            },
            'responsible_user.id': {
                'expected': int
            },
            'responsible_user.display_name': {
                'expected': str
            },
            'responsible_user.url': {
                'expected': Hyperlink
            },
            'responsible_teams': {
                'expected': list
            },
            'responsible_teams.0.id': {
                'expected': int
            },
            'responsible_teams.0.display_name': {
                'expected': str
            },
            'responsible_teams.0.url': {
                'expected': str
            },
            'public': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class knowledgeBaseAPIInheritedCases(
    knowledgeBaseAPITestCases,
):
    pass



@pytest.mark.module_assistance
class knowledgeBaseAPIPyTest(
    knowledgeBaseAPITestCases,
):

    pass
