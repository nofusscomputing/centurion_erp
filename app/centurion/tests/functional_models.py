import pytest



@pytest.mark.models
@pytest.mark.functional
class ModelTestCases:
    """Model Common Test Suite

    This test suite contains all of the functional common tests for **ALL**
    Centurion Models.

    For this test suite to function the following class attributes must be set
    for all classes that inherit from this class:

    - `kwargs_create_item: dict = {}`

        _Dict of the models fields and the values required for
        `model.objects.create()`_

    This attribute can either be a variable or a property. This attribute along
    with any prefixed `paremetized_` will be merged from each class in the
    inheritence chain. In addition this object must return a dict if defined.

    """


    @pytest.fixture( scope = 'function' )
    def created_model(self, request, django_db_blocker, model, user):

        if model._meta.abstract:

            yield None

        else:

            with django_db_blocker.unblock():

                model_object = model.objects.create(
                    **request.cls.kwargs_create_item
                )

                yield model_object



    @property
    def kwargs_create_item(self):
        return {}



    def test_model_created(self, model, created_model):
        """Model Created

        Ensure that the model exists within the Database
        """

        if model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )


        db_model = model.objects.get( id = created_model.id )

        assert db_model == created_model
