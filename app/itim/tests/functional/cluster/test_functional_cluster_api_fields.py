import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_cluster
class ClusterAPITestCases(
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

            for key, value in model_kwargs.items():

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
            kwargs_many_to_many.update({ 'devices': kwargs_many_to_many['nodes']})
            del kwargs_many_to_many['nodes']
            # del kwargs_many_to_many['target_team']

            kwargs.update({ 'parent_cluster': self.item})


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
            'parent_cluster': {
                'expected': dict
            },
            'parent_cluster.id': {
                'expected': int
            },
            'parent_cluster.display_name': {
                'expected': str
            },
            'parent_cluster.url': {
                'expected': Hyperlink
            },
            'cluster_type': {
                'expected': dict
            },
            'cluster_type.id': {
                'expected': int
            },
            'cluster_type.display_name': {
                'expected': str
            },
            'cluster_type.url': {
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'config': {
                'expected': dict
            },
            'config.config_key_1': {
                'expected': str
            },
            'nodes': {
                'expected': list
            },
            'nodes.0.id': {
                'expected': int
            },
            'nodes.0.display_name': {
                'expected': str
            },
            'nodes.0.url': {
                'expected': Hyperlink
            },
            'devices': {
                'expected': list
            },
            'devices.0.id': {
                'expected': int
            },
            'devices.0.display_name': {
                'expected': str
            },
            'devices.0.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class ClusterAPIInheritedCases(
    ClusterAPITestCases,
):
    pass



@pytest.mark.module_itim
class ClusterAPIPyTest(
    ClusterAPITestCases,
):

    pass
