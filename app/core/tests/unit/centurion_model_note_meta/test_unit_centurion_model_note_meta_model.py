import pytest

from core.tests.unit.centurion_sub_abstract.test_unit_centurion_sub_abstract_model import (
    CenturionSubAbstractModelInheritedCases,
)
from core.tests.unit.centurion_model_note.test_unit_centurion_model_note_model import (
    CenturionNoteModelInheritedCases,
)



@pytest.mark.meta_models
class MetaAbstractModelTestCases(
    CenturionNoteModelInheritedCases,
    CenturionSubAbstractModelInheritedCases,
):


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
    pass


    @pytest.mark.xfail( reason = 'This model does not require a tag')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_method_get_url_attribute__is_submodel_set(self, mocker, model_instance, audit_model):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        assert model_instance._is_submodel    # Test Failsafe. Confirm state

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        instance = audit_model()
        instance.id = 1

        model_instance.id = 1
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



    def test_method_get_url_kwargs(self, mocker, model_instance, audit_model):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        instance = audit_model()
        instance.id = 1

        model_instance.id = 1
        model_instance.model = instance

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'app_label': model_instance._meta.app_label,
            'model_name': str(model_instance._meta.model_name).replace('centurionmodelnote', ''),
            'model_id': model_instance.model.id,
            'pk': model_instance.id,
        }




class MetaAbstractModelPyTest(
    MetaAbstractModelTestCases,
):
    pass

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
