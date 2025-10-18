import pytest

from django.db import models

from uuid import UUID



@pytest.mark.models
@pytest.mark.functional
class ModelTestCases:
    """Model Common Test Suite

    This test suite contains all of the functional common tests for **ALL**
    Centurion Models.

    For this test suite to function the following fixtures must be available
    for this class:

    - model

    - model_kwargs

    Attribute prefixed `paremetized_` will be merged from each class in the
    inheritence chain. In addition this object must return a dict if defined.

    """


    @pytest.fixture( scope = 'function')
    def created_model(self, request, django_db_blocker,
        model, model_kwargs, mocker, model_user, kwargs_user
    ):

        item = None

        if not model._meta.abstract:

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


                item = model.objects.create(
                    **kwargs
                )

                for key, value in kwargs_many_to_many.items():

                    field = getattr(item, key)

                    for entry in value:

                        field.add(entry)

                request.cls.item = item

        yield item

        if item:

            with django_db_blocker.unblock():

                item.delete()



    def test_model_created(self, model, created_model):
        """Model Created

        Ensure that the model exists within the Database
        """

        if model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )


        db_model = model.objects.get( id = created_model.id )

        assert db_model == created_model



    @pytest.mark.regression
    def test_model_create_field_values(self,
        model, model_kwargs,
    ):
        """Check model fields

        When a model is created, ensure that the field data provided matches
        the created model field values.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract, test is N/A.' )

        kwargs = model_kwargs()

        for k, v in kwargs.copy().items():

            if(
                issubclass(getattr(getattr(model, k), 'field').__class__, models.ManyToManyField)
            ):
                del kwargs[k]

        obj = model.objects.create( **kwargs )

        failures = []

        for key, value in kwargs.items():

            if(
                issubclass(getattr(getattr(model, key), 'field').__class__, models.DateTimeField)
                or issubclass(getattr(getattr(model, key), 'field').__class__, models.DateField)
            ):
                continue

            field = getattr(obj, key)

            if(
                (
                    field != value
                    and not issubclass(field.__class__, UUID)
                ) or (
                    issubclass(field.__class__, UUID)
                    and str(field) != value
                )
            ):

                failures += [ f'field {key} value does not match {value}!={field}' ]


        assert len(failures) == 0, failures



    @pytest.mark.regression
    def test_model_edit_field_values(self,
        model, model_kwargs,
    ):
        """Check model fields

        When a model is edited, ensure that the field data provided matches
        the edited model field values.
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is abstract, test is N/A.' )

        kwargs_create = model_kwargs()

        for k, v in kwargs_create.copy().items():

            if(
                issubclass(getattr(getattr(model, k), 'field').__class__, models.ManyToManyField)
            ):
                del kwargs_create[k]

        obj = model.objects.create( **kwargs_create )


        kwargs_edit = model_kwargs()

        for k, v in kwargs_edit.copy().items():

            if(
                issubclass(getattr(getattr(model, k), 'field').__class__, models.ManyToManyField)
                or issubclass(getattr(getattr(model, k), 'field').__class__, models.DateTimeField)
                or issubclass(getattr(getattr(model, k), 'field').__class__, models.DateField)
                or k in [
                    'organization'
                ]
            ):
                del kwargs_edit[k]



        failures = []

        for key, value in kwargs_edit.items():

            field = getattr(obj, key)

            if issubclass(field.__class__, UUID):

                assert str(field) == kwargs_create[key], f'For test to be successful, field must be known value. {field}!={kwargs_create[key]}'

            else:
                assert field == kwargs_create[key], f'For test to be successful, field must be known value. {field}!={kwargs_create[key]}'

            setattr(obj, key, value)

            obj.save()

            field = getattr(obj, key)

            if(
                (
                    field != value
                    and not issubclass(field.__class__, UUID)
                ) or (
                    issubclass(field.__class__, UUID)
                    and str(field) != value
                )
            ):

                failures += [ f'field {key} value does not match {value}!={field}, edit failure.' ]


        assert len(failures) == 0, failures
