import pytest



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


    @pytest.fixture( scope = 'function' )
    def created_model(self, django_db_blocker, model, model_kwargs):

        if model._meta.abstract:

            yield None

        else:

            with django_db_blocker.unblock():

                model_object = model.objects.create(
                    **model_kwargs
                )

        yield model_object

        with django_db_blocker.unblock():

            model_object.delete()



    def test_model_created(self, model, created_model):
        """Model Created

        Ensure that the model exists within the Database
        """

        if model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )


        db_model = model.objects.get( id = created_model.id )

        assert db_model == created_model
