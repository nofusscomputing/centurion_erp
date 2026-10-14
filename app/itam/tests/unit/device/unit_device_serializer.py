import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_device
class DeviceSerializerTestCases(
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



    def test_serializer_validation_update_existing_invalid_name_starts_with_digit(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'starts with digit'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['name'] = '9dev-name'

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

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_name_contains_hyphon(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'contains hyphon'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['name'] = 'has_a_hyphon'

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

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_name_ends_with_dash(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid name 'ends with dash'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['name'] = 'ends-with-dash-'

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

        assert err.value.get_codes()['name'][0] == 'invalid_hostname'



    def test_serializer_validation_update_existing_invalid_uuid_first_octet(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet not hex'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = 'g0000000-0000-0000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



    def test_serializer_validation_update_existing_invalid_uuid_first_octet_wrong_length(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet wrong length'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '0000000-0000-0000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



    def test_serializer_validation_update_existing_invalid_uuid_second_octet(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet not hex'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-g000-0000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'


    def test_serializer_validation_update_existing_invalid_uuid_second_octet_wrong_length(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet wrong length'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-000-0000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



    def test_serializer_validation_update_existing_invalid_uuid_third_octet(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet not hex'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-g000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'


    def test_serializer_validation_update_existing_invalid_uuid_third_octet_wrong_length(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet wrong length'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-000-0000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



    def test_serializer_validation_update_existing_invalid_uuid_fourth_octet(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet not hex'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-0000-g000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'


    def test_serializer_validation_update_existing_invalid_uuid_fourth_octet_wrong_length(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet wrong length'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-0000-000-000000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



    def test_serializer_validation_update_existing_invalid_uuid_fifth_octet(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet not hex'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-0000-0000-g00000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'


    def test_serializer_validation_update_existing_invalid_uuid_fifth_octet_wrong_length(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet wrong length'
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['uuid'] = '00000000-0000-0000-0000-00000000000'

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

        assert err.value.get_codes()['uuid'][0] == 'invalid'



class DeviceSerializerInheritedCases(
    DeviceSerializerTestCases
):
    pass



@pytest.mark.module_itam
class DeviceSerializerPyTest(
    DeviceSerializerTestCases
):
    pass