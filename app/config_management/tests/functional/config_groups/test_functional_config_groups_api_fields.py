import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_configgroups
class ConfigGroupsAPITestCases(
    APIFieldsInheritedCases,
):

    @pytest.fixture( scope = 'class')
    def second_model(self, request, django_db_blocker,
        model, model_kwargs, model_device, kwargs_device
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

            device = model_device.objects.create( **kwargs_device() )

            kwargs_many_to_many.update({
                'hosts': [ device ]
            })

            kwargs.update({
                'parent': request.cls.item
            })


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

            device.delete()

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
            'parent': {
                'expected': dict
            },
            'parent.id': {
                'expected': int
            },
            'parent.display_name': {
                'expected': str
            },
            'parent.url': {
                'expected': str
            },
            'name': {
                'expected': str
            },
            'config': {
                'expected': dict
            },
            'config.key': {
                'expected': str
            },
            'config.existing': {
                'expected': str
            },

            'hosts': {
                'expected': list
            },
            'hosts.0.id': {
                'expected': int
            },
            'hosts.0.display_name': {
                'expected': str
            },
            'hosts.0.url': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class ConfigGroupsAPIInheritedCases(
    ConfigGroupsAPITestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupsAPIPyTest(
    ConfigGroupsAPITestCases,
):

    pass
