import pytest

from django.test import TestCase

from access.models.tenancy import TenancyManager
from access.models.tenancy import TenancyObject

from core.mixin.history_save import SaveHistory



class TenancyManagerTest(TestCase):

    item = TenancyManager


    def test_has_attribute_get_queryset(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'get_queryset')


    def test_is_function_get_queryset(self):
        """ Attribute 'get_organization' is a function """
        
        assert callable(self.item.get_queryset)



class TenancyObjectTestCases:

    item = TenancyObject


    def test_class_inherits_save_history(self):
        """ Confirm class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(TenancyObject, SaveHistory)


    def test_has_attribute_history_app_label(self):
        """ Attribute history_app_name exists """
        
        assert hasattr(self.item, 'history_app_label')


    def test_has_attribute_history_model_name(self):
        """ Attribute history_model_name exists """
        
        assert hasattr(self.item, 'history_model_name')


    def test_has_attribute_kb_model_name(self):
        """Attribute _kb_model_name exists """
        
        assert hasattr(self.item, 'kb_model_name')


    def test_has_attribute_organization(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'organization')


    def test_has_attribute_is_global(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'is_global')


    def test_has_attribute_model_notes(self):
        """ Field organization exists """
        
        assert hasattr(self.item, 'model_notes')


    def test_has_attribute_note_basename(self):
        """ Attribute note_basename exists """
        
        assert hasattr(self.item, 'note_basename')


    def test_has_attribute_get_organization(self):
        """ Function 'get_organization' Exists """
        
        assert hasattr(self.item, 'get_organization')


    def test_is_function_get_organization(self):
        """ Attribute 'get_organization' is a function """
        
        assert callable(self.item.get_organization)


    @pytest.mark.skip(reason="figure out how to test abstract class")
    def test_has_attribute_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        assert 'objects' in self.item


    @pytest.mark.skip(reason="figure out how to test abstract class")
    def test_attribute_not_none_objects(self):
        """ Attribute Check

        attribute `objects` must be set to `access.models.TenancyManager()`
        """

        assert self.item.objects is not None


    @pytest.mark.skip(reason="write test")
    def test_field_not_none_organzation(self):
        """ Ensure field is set

        Field organization must be defined for all tenancy objects
        """

        assert self.item.objects is not None



class TenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):

    pass