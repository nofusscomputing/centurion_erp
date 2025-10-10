import pytest

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView



@pytest.mark.model_knowledgebasecategory
class knowledgebaseCategorySerializerTestCases(
    SerializerTestCases
):

    @pytest.fixture( scope = 'function' )
    def created_model(self, django_db_blocker, model, model_kwargs):

        with django_db_blocker.unblock():

            item = model.objects.create( **model_kwargs() )

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
                data = kwargs
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'



    def test_serializer_validation_parent_category_not_self(self,
        created_model,
        model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that you cant assisgn self as parent category
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
                    "parent_category": created_model.id
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['parent_category'][0] == 'parent_category_not_self'



    def test_serializer_validation_both_target_team_target_user(self,
        kwargs_api_create, model, model_serializer, request_user,
        model_group, kwargs_group
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
        group = model_group.objects.create( **kwargs_group() )
        kwargs.update({
            'target_team': [ group.id ]
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

        group.delete()
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
        del kwargs['target_user']

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



    def test_serializer_validation_update_existing_target_team(self,
        created_model,
        model, model_serializer, request_user,
        model_group, kwargs_group
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

        group = model_group.objects.create( **kwargs_group() )

        with pytest.raises(ValidationError) as err:

            serializer = model_serializer['model'](
                created_model,
                context = {
                    'request': mock_view.request,
                    'view': mock_view,
                },
                data={
                    "target_team": [ group.id ]
                },
                partial=True,
            )

            serializer.is_valid(raise_exception = True)

        group.delete()

        assert err.value.get_codes()['non_field_errors'][0] == 'invalid_not_both_target_team_user'


    def test_serializer_validation_update_existing_target_user(self,
        created_model,
        model, model_serializer, request_user,
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

        group = model_group.objects.create( **kwargs_group() )
        created_model.target_user = None
        created_model.target_team.add( group )
        created_model.save()

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




class knowledgebaseCategorySerializerInheritedCases(
    knowledgebaseCategorySerializerTestCases
):
    pass



@pytest.mark.module_assistance
class knowledgebaseCategorySerializerPyTest(
    knowledgebaseCategorySerializerTestCases
):
    pass