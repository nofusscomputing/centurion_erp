from django.db import models
from django.test import TestCase

from core.mixin.history_save import SaveHistory



class SaveHistoryMixinTestCases:

    item = None
    """Instaniated Model to test
    
    Population of this field should be done during test setup by creating an object
    """

    model = None
    """Model to test"""



    def test_class_inherits_django_models(self):
        """ Class inheritence

        Model must inherit SaveHistory
        """

        assert issubclass(self.model, models.Model)



    def test_class_inherits_save_history(self):
        """ Class inheritence

        Model must inherit SaveHistory
        """

        assert issubclass(self.model, SaveHistory)


    def test_attribute_exist_save_model_history(self):
        """Attribute Exists

        `save_model_history` must exist
        """

        assert hasattr(self.item.__class__, 'save_model_history')


    def test_attribute_type_save_model_history(self):
        """Attribute Type

        `save_model_history` must be of type bool
        """

        assert type(self.item.__class__.save_model_history) is bool


    def test_attribute_exist_fields(self):
        """Attribute Exists

        `fields` must exist
        """

        assert hasattr(self.item.__class__, 'fields')


    def test_attribute_type_fields(self):
        """Attribute Type

        `fields` must be of type list
        """

        assert type(self.item.fields) is list


    def test_attribute_exist_save_history(self):
        """Attribute Exists

        `save_history` must exist
        """

        assert hasattr(self.item.__class__, 'save_history')


    def test_function_callable_save_history(self):
        """ Function Check

        function `save_history()` must exist
        """

        assert callable(self.item.__class__.save_history)



class SaveHistoryMixinInheritedCases(
    SaveHistoryMixinTestCases,
):

    item = None
    """Instaniated Model to test
    
    Population of this field should be done during test setup by creating an object
    """

    model = None
    """Model to test"""

    def test_class_save_history_function_called_delete(self):
        """Test Function Called

        `delete` function must be called when object is deleted
        """

        pass

    def test_class_save_history_function_called_save(self):
        """Test Function Called

        `save` function must be called when object is created and modified
        """

        pass



class SaveHistoryMixinTest(
    SaveHistoryMixinTestCases,
    TestCase,
):

    model = SaveHistory


    @classmethod
    def setUpTestData(self):

        class MockModel(self.model):

            class Meta:

                app_label = 'core'

                verbose_name = 'unit test'

        self.item = MockModel()



    def test_attribute_exist_delete(self):
        """Attribute Exists

        `delete` must exist
        """

        assert hasattr(self.item.__class__, 'delete')


    def test_function_callable_delete(self):
        """ Function Check

        function `delete()` must exist
        """

        assert callable(self.item.__class__.delete)



    def test_attribute_exist_save(self):
        """Attribute Exists

        `save` must exist
        """

        assert hasattr(self.item.__class__, 'save')


    def test_function_callable_save(self):
        """ Function Check

        function `save()` must exist
        """

        assert callable(self.item.__class__.save)
