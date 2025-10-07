import pytest

from django.db import models



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
