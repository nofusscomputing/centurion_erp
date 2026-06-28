import pytest

from django.db import models

# from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_usersettings
class UserSettingsSerializerTestCases(
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


    @pytest.mark.regression
    def test_serializer_create_calls_model_full_clean(self, created_model,
        kwargs_api_create, mocker, model, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that using valid data the object validates without exceptions.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        serializer = model_serializer['model'](
            created_model,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create,
            partial = True,
        )

        serializer.is_valid(raise_exception = True)

        full_clean = mocker.spy(model, 'full_clean')

        serializer.save()

        full_clean.assert_called_once()



    def test_only_base_defines__urls_object(self,
        model_serializer,
    ):
        """BaseSerializer field check

        ensure that the `get_url_fields` is the method name to be called.
        """

        assert model_serializer['model']._declared_fields['_urls'].method_name == 'get_url'



class UserSettingsSerializerInheritedCases(
    UserSettingsSerializerTestCases
):
    pass



@pytest.mark.module_settings
class UserSettingsSerializerPyTest(
    UserSettingsSerializerTestCases
):
    pass