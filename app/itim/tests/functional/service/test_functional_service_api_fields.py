import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_service
class ServiceAPITestCases(
    APIFieldsInheritedCases,
):


    @pytest.fixture( scope = 'class')
    def second_model(self, request, django_db_blocker,
        model, model_kwargs, model_cluster, kwargs_cluster
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

            dep_kwargs = model_kwargs.copy()
            dep_kwargs['name'] = 'dep service'
            ports = dep_kwargs['port']
            del dep_kwargs['port']
            dependent_service = model.objects.create( **dep_kwargs )

            for port in ports:
                dependent_service.port.add( port )

            template_kwargs = model_kwargs.copy()
            template_kwargs['name'] = 'a template'
            del template_kwargs['port']
            template = model.objects.create( **template_kwargs )

            kwargs_many_to_many.update({ 'dependent_service': [ dependent_service ]})

            clu_kwargs = kwargs_cluster.copy()
            nodes = clu_kwargs['nodes']
            del clu_kwargs['nodes']
            cluster = model_cluster.objects.create( **clu_kwargs )

            for node in nodes:
                cluster.nodes.add( node )

            kwargs.update({
                'cluster': cluster,
                'template': template,
            })
            del kwargs['device']


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
            cluster.delete()
            template.delete()

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
            'is_template': {
                'expected': bool
            },
            'template': {
                'expected': dict
            },
            'template.id': {
                'expected': int
            },
            'template.display_name': {
                'expected': str
            },
            'template.url': {
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'device': {
                'expected': dict
            },
            'device.id': {
                'expected': int
            },
            'device.display_name': {
                'expected': str
            },
            'device.url': {
                'expected': Hyperlink
            },
            'cluster': {
                'expected': dict
            },
            'cluster.id': {
                'expected': int
            },
            'cluster.display_name': {
                'expected': str
            },
            'cluster.url': {
                'expected': Hyperlink
            },
            'config': {
                'expected': dict
            },
            'config.config_key_1': {
                'expected': str
            },
            'config_key_variable': {
                'expected': str
            },
            'port': {
                'expected': list
            },
            'port.0.id': {
                'expected': int
            },
            'port.0.display_name': {
                'expected': str
            },
            'port.0.url': {
                'expected': Hyperlink
            },
            'dependent_service': {
                'expected': list
            },
            'dependent_service.0.id': {
                'expected': int
            },
            'dependent_service.0.display_name': {
                'expected': str
            },
            'dependent_service.0.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class ServiceAPIInheritedCases(
    ServiceAPITestCases,
):
    pass



@pytest.mark.module_itim
class ServiceAPIPyTest(
    ServiceAPITestCases,
):

    pass
