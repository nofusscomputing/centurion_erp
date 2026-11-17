import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.serializers.common import CommonModelSerializer
from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_cluster
class ClusterSerializerTestCases(
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



    def test_serializer_validation_self_not_parent(self,
        created_model, mocker,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if assiging itself as parent a validation error occurs
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

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
                    "parent_cluster":created_model.id,
                },
                partial = True
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent_cluster'] == 'parent_not_self'



    @pytest.mark.regression
    def test_serializer_update_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_serializer, request_user,
        created_model,
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PUT) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        instance = created_model

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'update',
        )

        mock_view.kwargs = instance.get_url_kwargs()

        serializer = model_serializer['model'](
            instance = instance,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

        serializer.save()

        del mock_view.kwargs

        full_clean.assert_called_once()



    @pytest.mark.regression
    def test_serializer_partial_update_calls_common_validate(self,
        mocker, model, model_serializer, request_user,
        created_model,
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PATCH) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        instance = created_model

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'partial_update',
        )

        mock_view.kwargs = instance.get_url_kwargs()

        serializer = model_serializer['model'](
            instance = instance,
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = {
                'model_notes': "update data"
            },
            partial = True
        )

        full_clean = mocker.spy(CommonModelSerializer, 'validate')

        serializer.is_valid(raise_exception = True)

        serializer.save()

        del mock_view.kwargs

        full_clean.assert_called_once()



class ClusterSerializerInheritedCases(
    ClusterSerializerTestCases
):
    pass



@pytest.mark.module_itim
class ClusterSerializerPyTest(
    ClusterSerializerTestCases
):
    pass