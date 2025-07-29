import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_configgroups
class ConfigGroupsSerializerTestCases(
    SerializerTestCases
):
    pass

    @pytest.fixture( scope = 'function' )
    def created_model(self, django_db_blocker, model, model_kwargs):

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



    def test_serializer_validation_update_existing_parnet_not_self(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is assigned itself as it's parent group
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['parent'] = created_model.id

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                created_model,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs,
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent'][0] == 'self_not_parent'


    def test_serializer_validation_update_existing_invalid_config_key(self,
        created_model,
        model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item has it's config updated with an invalid config key
        a validation exception is raised.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                created_model,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    "config": {'software': 'is invalid'}
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['config'][0] == 'invalid'



class ConfigGroupsSerializerInheritedCases(
    ConfigGroupsSerializerTestCases
):
    pass



@pytest.mark.module_config_management
class ConfigGroupsSerializerPyTest(
    ConfigGroupsSerializerTestCases
):
    pass