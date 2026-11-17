import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.serializers.common import CommonModelSerializer
from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_knowledgebase
class KnowledgeBaseSerializerTestCases(
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
    def test_serializer_update_calls_common_validate(self,
        kwargs_api_create, mocker, model, model_kwargs, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PUT) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        kwargs = model_kwargs()

        target_team = kwargs['target_team']

        del kwargs['target_team']

        instance = model.objects.create( **kwargs )

        instance.target_team.add(target_team[0])

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
        mocker, model, model_kwargs, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that when updating (HTTP/PATCH) an object `validate()` is called.
        """

        mocker.patch.object(request_user, 'has_perm', return_value = True)

        mocker.patch.object(request_user, 'has_perms', return_value = True)

        kwargs = model_kwargs()

        target_team = kwargs['target_team']

        del kwargs['target_team']

        instance = model.objects.create( **kwargs )

        instance.target_team.add(target_team[0])

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



    def test_serializer_validation_no_title(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating and no title is provided a validation error occurs
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['title']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['title'][0] == 'required'



    def test_serializer_validation_both_target_team_target_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that both target user and target team raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs.update({
            'target_user': request_user.id
        })

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'



    def test_serializer_validation_no_target_team_target_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if either target user and target team is missing it raises validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        del kwargs['target_team']

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_need_target_team_or_user'



    def test_serializer_validation_update_existing_target_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if an existing item with target user is updated to include a target_team
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                self.item_has_target_user,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    "target_team": [ self.add_team.id ]
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'


    def test_serializer_validation_update_existing_target_user(self,
        created_model,
        kwargs_api_create, model, model_serializer, request_user,
        model_group, kwargs_group
    ):
        """Serializer Validation Check

        Ensure that if an existing item with target team is updated to include a target_user
        it raises a validation error
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        group = model_group.objects.create( **kwargs_group() )
        kwargs.update({
            'target_team': [ group ]
        })

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                created_model,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    "target_user": request_user.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        group.delete()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'




class KnowledgeBaseSerializerInheritedCases(
    KnowledgeBaseSerializerTestCases
):
    pass



@pytest.mark.module_assistance
class KnowledgeBaseSerializerPyTest(
    KnowledgeBaseSerializerTestCases
):
    pass