import inspect
import pytest

from django.core.exceptions import (
    ValidationError
)

from core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model import (
    CenturionSubAbstractModelInheritedCases,
)
from core.tests.unit.centurion_model_note.test_unit_centurion_model_note_model import (
    CenturionNoteModelInheritedCases,
)



@pytest.mark.meta_models
class MetaAbstractModelTestCases(
    CenturionSubAbstractModelInheritedCases,
    CenturionNoteModelInheritedCases,
):



    def test_method_centurionnotes_clean_fields_called(self, mocker, model_instance):
        """Test Class Method

        Ensure method `core.models.centurion.CenturionModel.delete()` is called
        when `model.delete()` is called.
        """

        clean_fields = mocker.patch('core.models.centurion_notes.NoteMetaModel.clean_fields', return_value = None)

        model_instance.clean_fields()

        clean_fields.assert_called_once()



    def test_method_centurionnotes_clean_fields_no_model_exception(self, mocker, model_instance):
        """Test Class Method

        Ensure method `core.models.centurion.CenturionModel.delete()` is called
        when `model.delete()` is called.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()
        model_instance.model = None

        with pytest.raises( ValidationError ) as e:

            model_instance.clean_fields()

        assert e.value.code == 'no_model_supplied'



    def test_method_get_url_attribute__is_submodel_set(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        assert model_instance._is_submodel    # Test Failsafe. Confirm state

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        model_instance.id = 1

        model_instance.model = model_instance

        url_basename = f'v2:_api_centurionmodelnote_sub-detail'

        url = model_instance.get_url( relative = True)

        reverse.assert_called_with(
            url_basename,
            None,
            {
                'app_label': model_instance._meta.app_label,
                'model_name': model_instance._meta.model_name,
                'model_id': 1,
                'pk': 1
            },
            None,
            None
        )



class MetaAbstractModelInheritedCases(
    MetaAbstractModelTestCases,
):
    # pass


    @pytest.mark.xfail( reason = 'This model does not require a tag')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_method_get_url_attribute__is_submodel_set(self, mocker, model_instance, note_model):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        assert model_instance._is_submodel    # Test Failsafe. Confirm state

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        instance = note_model()
        instance.id = 1

        model_instance.model = instance

        url_basename = f'v2:_api_centurionmodelnote_sub-detail'

        url = model_instance.get_url( relative = True)

        reverse.assert_called_with(
            url_basename,
            None,
            {
                'app_label': model_instance._meta.app_label,
                'model_name': str(model_instance._meta.model_name).replace('centurionmodelnote', ''),
                'model_id': 1,
                'pk': 1
            },
            None,
            None
        )



    def test_method_get_url_kwargs(self, mocker, model_instance, note_model):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        instance = note_model()
        instance.id = 1

        model_instance.model = instance

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'app_label': model_instance._meta.app_label,
            'model_name': str(model_instance._meta.model_name).replace('centurionmodelnote', ''),
            'model_id': model_instance.model.id,
            'pk': model_instance.id,
        }


    def test_method_centurionnotes_clean_fields_no_errors(self, mocker, model_instance, note_model, organization_one):
        """Test Class Method

        Ensure method `core.models.centurion_notes.NoteMetaModel.clean_fields()` throws no errors
        when called.
        """

        clean_fields = mocker.patch('core.models.centurion_notes.CenturionModelNote.clean_fields', return_value = None)

        instance = note_model()
        instance.id = 1
        instance.organization = organization_one

        model_instance.model = instance

        model_instance.clean_fields()



class MetaAbstractModelPyTest(
    MetaAbstractModelTestCases,
):


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        model_instance.model = model_instance

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'app_label': model_instance._meta.app_label,
            'model_name': model_instance._meta.model_name,
            'model_id': model_instance.model.id,
            'pk': model_instance.id,
        }


    @pytest.mark.xfail( reason = 'This model is an abstract model')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_model_is_abstract(self, model):

        assert model._meta.abstract

    def test_model_not_proxy(self, model):

        assert not model._meta.proxy


    def test_model_creation(self):
        """
        This test is a duplicate of a test with the same name. As this model
        is an abstract model this test is not required.
        """
        pass


    def test_method_clean_fields_default_attributes(self, model_instance):
        """Test Class Method
        
        Ensure method `clean_fields`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.clean_fields)

        exclude = sig.parameters['exclude'].default

        assert(
            exclude == None
        )
