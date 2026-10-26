import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_service
class ServiceSerializerTestCases(
    SerializerTestCases
):


    @pytest.fixture( scope = 'function' )
    def created_model(self, django_db_blocker, model, model_kwargs):

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


            item = model.objects.create( **kwargs )

            for key, value in kwargs_many_to_many.items():

                field = getattr(item, key)

                for entry in value:

                    field.add(entry)

            yield item

            item.delete()



    def test_serializer_validation_no_name(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['name']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_can_create_device(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that a valid item is serialized
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs,
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_port(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no port is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['port']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['port'][0] == 'required'



    def test_serializer_validation_no_port_required_if_template_with_port(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_kwargs,
    ):
        """Serializer Validation Check

        Ensure that if creating and no port is provided and the template has a port
        no validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = model_kwargs()
        kwargs['is_template'] = True
        ports = kwargs['port']
        del kwargs['port']

        template = model.objects.create( **kwargs )

        for port in ports:
            template.port.add( port )


        kwargs = kwargs_api_create.copy()
        kwargs['is_template'] = False
        kwargs['template'] = template.id
        del kwargs['port']

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs
        )

        assert serializer.is_valid(raise_exception = True)
        template.delete()



    def test_serializer_validation_template_without_port(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_kwargs
    ):
        """Serializer Validation Check

        Ensure that if creating a port is provided and the template has no port
        no validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = model_kwargs()
        kwargs['is_template'] = True
        del kwargs['port']

        template = model.objects.create( **kwargs )

        kwargs = kwargs_api_create.copy()
        kwargs['is_template'] = False
        kwargs['template'] = template.id


        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs
        )

        assert serializer.is_valid(raise_exception = True)
        template.delete()



    def test_serializer_validation_no_port_or_template_port(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_kwargs,
    ):
        """Serializer Validation Check

        Ensure that if creating and no port is provided and the template
        has no port a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = model_kwargs()
        kwargs['is_template'] = True
        del kwargs['port']
        del kwargs['device']

        template = model.objects.create( **kwargs )

        kwargs = kwargs_api_create.copy()
        kwargs['is_template'] = False
        kwargs['template'] = template.id
        del kwargs['port']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['port'][0] == 'required'
        template.delete()



    def test_serializer_validation_no_device(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no device is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['device']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'one_of_cluster_or_device'



    def test_serializer_validation_device_and_cluster(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_cluster, kwargs_cluster
    ):
        """Serializer Validation Check

        Ensure that if creating and a cluster and device is provided
        a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_cluster()
        nodes = kwargs['nodes']
        del kwargs['nodes']
        cluster = model_cluster.objects.create( **kwargs )

        for node in nodes:
            cluster.nodes.add( node )

        kwargs = kwargs_api_create.copy()
        kwargs['cluster'] = cluster.id


        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'either_cluster_or_device'
        cluster.delete()



    def test_serializer_validation_no_circular_dependency(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user,
        model_kwargs
    ):
        """Serializer Validation Check

        Ensure that if creating and a dependent service loop
        a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = model_kwargs()
        del kwargs['port']
        root_service = model.objects.create ( **kwargs )
        root_service.dependent_service.add( created_model )


        kwargs = kwargs_api_create.copy()
        kwargs['dependent_service'] = [ root_service.id ]

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                created_model,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
                partial = True
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['dependent_service'][0] == 'no_circular_dependencies'
        root_service.delete()



class ServiceSerializerInheritedCases(
    ServiceSerializerTestCases
):
    pass



@pytest.mark.module_itim
class ServiceSerializerPyTest(
    ServiceSerializerTestCases
):
    pass