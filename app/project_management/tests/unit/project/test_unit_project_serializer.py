import pytest

from django.db import models

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)

from centurion.tests.abstract.mock_view import MockView
from project_management.serializers.project import (
    Project,
)



@pytest.mark.model_project
class ProjectSerializerTestCases(
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


    def test_serializer_validation_external_ref_not_import_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

        Ensure that if creating by user who is not import user, they can't edit
        fields external_ref and external_system.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['external_ref'] = 1,
        kwargs['external_system'] = int(Project.Ticket_ExternalSystem.CUSTOM_1)

        mock_view.is_import_user = False


        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs,
        )

        serializer.is_valid(raise_exception = True)

        serializer.save()

        assert serializer.instance.external_ref is None and serializer.instance.external_system is None



    def test_serializer_validation_external_ref_is_import_user(self,
        kwargs_api_create, model, model_serializer, request_user
    ):
        """Serializer Validation Check

         Ensure that if creating by user who import user, they can edit
        fields external_ref and external_system.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        kwargs = kwargs_api_create.copy()
        kwargs['external_ref'] = 1
        kwargs['external_system'] = int(Project.Ticket_ExternalSystem.CUSTOM_1)

        mock_view.is_import_user = True


        serializer = model_serializer['import'](
           context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs,
        )

        serializer.is_valid(raise_exception = True)

        serializer.save()

        assert (
            serializer.instance.external_ref == 1 and 
            serializer.instance.external_system == int(Project.Ticket_ExternalSystem.CUSTOM_1)
        )



class ProjectSerializerInheritedCases(
    ProjectSerializerTestCases
):
    pass



@pytest.mark.module_project_management
class ProjectSerializerPyTest(
    ProjectSerializerTestCases
):
    pass