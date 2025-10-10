import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_featureflag
class FeatureFlagSerializerTestCases(
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



    def test_serializer_validation_no_name_exception(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating and field name is not provided a
        validation error occurs
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
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'


    def test_serializer_validation_no_software_exception(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating and field software is not provided, no
        validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['software']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'][0] == 'required'


    def test_serializer_validation_feature_flagging_not_enabled(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_software, kwargs_software,
    ):
        """Serializer Validation Check

        Ensure that when creating and the software doesn't, have feature
        flagging enabled an exception is thrown.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_software()
        kwargs['name'] = 'ff_soft'
        software = model_software.objects.create( **kwargs )

        kwargs = kwargs_api_create.copy()
        kwargs['software'] = software.id

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'] == 'feature_flagging_disabled'
        software.delete()


    def test_serializer_validation_feature_flagging_not_enabled_for_organization(self,
        kwargs_api_create, model, model_serializer, request_user, api_request_permissions
    ):
        """Serializer Validation Check

        Ensure that when creating and the software doesn't, have feature
        flagging enabled an exception is thrown.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['organization'] = api_request_permissions['tenancy']['different']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['organization'] == 'feature_flagging_wrong_organizaiton'



    def test_serializer_validation_no_description_ok(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating and field description is not provided, no
        validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['description']

        serializer = model_serializer['model'](
            data = kwargs
        )

        assert serializer.is_valid(raise_exception = True)



    def test_serializer_validation_no_enabled_ok_default_false(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that when creating and field enabled is not provided, no
        validation error occurs and enabled is set to `false`
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['enabled']

        serializer = model_serializer['model'](
            data = kwargs
        )

        assert serializer.is_valid(raise_exception = True)

        serializer.save()

        assert serializer.instance.enabled is False



class FeatureFlagSerializerInheritedCases(
    FeatureFlagSerializerTestCases
):
    pass



@pytest.mark.module_devops
class FeatureFlagSerializerPyTest(
    FeatureFlagSerializerTestCases
):
    pass