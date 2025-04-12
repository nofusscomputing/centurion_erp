import pytest

from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch

from access.models.organization import Organization
from access.models.tenancy import TenancyManager
from access.models.tenancy import (
    TenancyObject,
)

from core.lib.feature_not_used import FeatureNotUsed
from core.tests.unit.mixin.test_unit_history_save import (
    SaveHistory,
    SaveHistoryMixinInheritedCases
)



class ModelManagerTestCases:
    """ Test cases for Model Abstract Classes """

    manager = TenancyManager


    def test_model_class_tenancy_manager_function_get_queryset(self):
        """ Function Check

        function `get_queryset()` must exist
        """

        assert hasattr(self.model.objects, 'get_queryset')

        assert callable(self.model.objects.get_queryset)


    def test_model_class_tenancy_manager_function_get_queryset_called(self):
        """ Function Check

        function `access.models.TenancyManager.get_queryset()` within the Tenancy manager must
        be called as this function limits queries to the current users organizations.
        """

        with patch.object(self.manager, 'get_queryset', side_effect = self.model.objects.get_queryset, return_value = []) as patched:

            model = self.model

            patched.reset_mock()

            model.objects.filter()

            assert patched.called



    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_manager_results_get_queryset(self):
        """ Function Results Check

        function `get_queryset()` must not return data from any organization the user is
        not part of.
        """

        pass


    @pytest.mark.skip(reason="write test")
    def test_model_class_tenancy_manager_results_get_queryset_super_user(self):
        """ Function Results Check

        function `get_queryset()` must return un-filtered data for super-user.
        """

        pass



class TenancyObjectTestCases(
    ModelManagerTestCases,
    SaveHistoryMixinInheritedCases,
):
    """Test Cases for access.models.tenancy.TenancyObject"""


    model = TenancyObject

    item = None
    """Instaniated Model to test
    
    Population of this field should be done during test setup by creating an object
    """



    # @classmethod
    # def setUpTestData(self):

    #     class TestModel(self.model):

    #         pass


    #     if self.item is None:

    #         self.item = TestModel()




    def test_class_inherits_tenancy_object(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TenancyObject)



    def test_class_inherits_save_history(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, SaveHistory)



    def test_attribute_exist_objects(self):
        """Attribute Exists

        `objects` must exist
        """

        assert hasattr(self.item.__class__, 'objects')


    def test_attribute_type_objects(self):
        """Attribute Exists

        `objects` must exist
        """

        assert type(self.item.__class__.objects) is self.manager



    def test_field_exist_id(self):
        """Model Field Exists

        id must exist
        """

        assert hasattr(self.model, 'id')


    # def test_field_type_id(self):
    #     """Model Field Type

    #     organizatidon is of type str
    #     """

    #     assert type(self.model.id) is django_models.ForeignKey



    def test_field_exist_organization(self):
        """Model Field Exists

        organization must exist
        """

        assert hasattr(self.model, 'organization')


    # def test_field_type_organization(self):
    #     """Model Field Type

    #     organization is of type str
    #     """

    #     assert type(self.model.organization) is django_models.ForeignKey



    def test_field_exist_is_global(self):
        """Model Field Exists

        is_global must exist
        """

        assert hasattr(self.model, 'is_global')


    # def test_field_type_is_global(self):
    #     """Model Field Type

    #     is_global is of type str
    #     """

    #     assert type(self.model.is_global) is django_models.BooleanField



    def test_field_exist_model_notes(self):
        """Model Field Exists

        model_notes must exist
        """

        assert hasattr(self.model, 'model_notes')


    # def test_field_type_model_notes(self):
    #     """Model Field Type

    #     model_notes is of type str
    #     """

    #     assert type(self.model.model_notes) is django_models.BooleanField



    def test_attribute_get_organization(self):
        """Attribute Exists

        get_organization must exist
        """

        assert hasattr(self.model, 'get_organization')


    def test_function_callable_get_organization(self):
        """Attribute is a function

        get_organization must be a function (callable)
        """

        assert callable(self.model.get_organization)


    def test_attribute_type_get_organization(self):
        """Attribute Type

        get_organization is of type str
        """

        assert type(self.item.get_organization()) is Organization



    def test_attribute_exist_app_namespace(self):
        """Attribute Exists

        app_namespace must exist
        """

        assert hasattr(self.model, 'app_namespace')


    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert self.model.app_namespace is None


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace is None



    def test_attribute_exist_history_app_label(self):
        """Attribute Exists

        history_app_label must exist
        """

        assert hasattr(self.model, 'history_app_label')


    def test_attribute_type_history_app_label(self):
        """Attribute Type

        history_app_label is of type str
        """

        assert self.model.history_app_label is None


    def test_attribute_value_history_app_label(self):
        """Attribute Type

        history_app_label has been set, override this test case with the value
        of attribute `history_app_label`
        """

        assert self.model.history_app_label is None



    def test_attribute_exist_history_model_name(self):
        """Attribute Exists

        history_model_name must exist
        """

        assert hasattr(self.model, 'history_app_label')


    def test_attribute_type_history_model_name(self):
        """Attribute Type

        history_model_name is of type str
        """

        assert self.model.history_model_name is None


    def test_attribute_value_history_model_name(self):
        """Attribute Type

        history_model_name has been set, override this test case with the value
        of attribute `history_model_name`
        """

        assert self.model.history_model_name is None



    def test_attribute_exist_kb_model_name(self):
        """Attribute Exists

        kb_model_name must exist
        """

        assert hasattr(self.model, 'kb_model_name')


    def test_attribute_type_kb_model_name(self):
        """Attribute Type

        kb_model_name is of type str
        """

        assert self.model.kb_model_name is None


    def test_attribute_value_kb_model_name(self):
        """Attribute Type

        kb_model_name has been set, override this test case with the value
        of attribute `kb_model_name`
        """

        assert self.model.kb_model_name is None



    def test_attribute_exist_note_basename(self):
        """Attribute Exists

        note_basename must exist
        """

        assert hasattr(self.model, 'note_basename')


    def test_attribute_type_note_basename(self):
        """Attribute Type

        note_basename is of type str
        """

        assert self.model.note_basename is None


    def test_attribute_value_note_basename(self):
        """Attribute Type

        note_basename has been set, override this test case with the value
        of attribute `note_basename`
        """

        assert self.model.note_basename is None



    def test_attribute_get_page_layout(self):
        """Attribute Exists

        page_layout must exist
        """

        assert hasattr(self.model, 'get_page_layout')


    def test_function_callable_get_page_layout(self):
        """Attribute is a function

        page_layout must be a function (callable)
        """

        assert callable(self.model.get_page_layout)


    def test_attribute_type_get_page_layout(self):
        """Attribute Type

        get_page_layout is of type list
        """

        assert type(self.item.get_page_layout()) is list



    def test_attribute_get_get_app_namespace(self):
        """Attribute Exists

        get_app_namespace must exist
        """

        assert hasattr(self.model, 'get_app_namespace')


    def test_function_callable_get_app_namespace(self):
        """Attribute is a function

        get_app_namespace must be a function (callable)
        """

        assert callable(self.model.get_app_namespace)


    def test_attribute_type_get_app_namespace(self):
        """Attribute Type

        get_app_namespace is of type str
        """

        assert type(self.item.get_app_namespace()) is str



    def test_attribute_get_url(self):
        """Attribute Exists

        get_url must exist
        """

        assert hasattr(self.model, 'get_url')


    def test_function_callable_get_url(self):
        """Attribute is a function

        get_url must be a function (callable)
        """

        assert callable(self.model.get_url)


    def test_attribute_type_get_url(self):
        """Attribute Type

        get_url is of type str
        """

        assert type(self.item.get_url()) is str



    def test_attribute_get_url_kwargs(self):
        """Attribute Exists

        get_url_kwargs must exist
        """

        assert hasattr(self.model, 'get_url_kwargs')


    def test_function_callable_get_url_kwargs(self):
        """Attribute is a function

        get_url_kwargs must be a function (callable)
        """

        assert callable(self.model.get_url)


    def test_attribute_type_get_url_kwargs(self):
        """Attribute Type

        get_url_kwargs is of type dict
        """

        assert type(self.item.get_url_kwargs()) is dict



    def test_attribute_exists_get_url_kwargs_notes(self):
        """Test for existance of field in `<model>`

        Attribute `get_url_kwargs_notes` must be defined in class.
        """

        obj = getattr(self.item, 'get_url_kwargs_notes', None)

        if callable(obj):

            obj = obj()

        if(
            not str(self.model._meta.model_name).lower().endswith('notes')
            and obj is not FeatureNotUsed
        ):

            assert hasattr(self.item, 'get_url_kwargs_notes')

        else:

            print('Test is n/a')

            assert True



    def test_attribute_callable_get_url_kwargs_notes(self):
        """Test field `<model>` callable

        Attribute `get_url_kwargs_notes` must be a function
        """

        obj = getattr(self.item, 'get_url_kwargs_notes', None)

        if callable(obj):

            obj = obj()

        if(
            not str(self.model._meta.model_name).lower().endswith('notes')
            and obj is not FeatureNotUsed
        ):

            assert callable(self.item.get_url_kwargs_notes)

        else:

            print('Test is n/a')

            assert True



    def test_attribute_type_get_url_kwargs_notes(self):
        """Test field `<model>`type

        Attribute `get_url_kwargs_notes` must be dict
        """

        obj = getattr(self.item, 'get_url_kwargs_notes', None)

        if callable(obj):

            obj = obj()

        if(
            not str(self.model._meta.model_name).lower().endswith('notes')
            and obj is not FeatureNotUsed
        ):

            assert type(self.item.get_url_kwargs_notes()) is dict

        else:

            print('Test is n/a')

            assert True



    def test_attribute_exists_table_fields(self):
        """Attrribute Test, Exists

        Ensure attribute `table_fields` exists
        """

        assert hasattr(self.item, 'table_fields')


    def test_attribute_type_table_fields(self):
        """Attrribute Test, Type

        Ensure attribute `table_fields` is of type `list`
        """

        assert type(self.item.table_fields) is list



class TenancyObjectInheritedCases(
    TenancyObjectTestCases
):
    """Test Cases for models that inherit from

    **Note:** dont use these test cases use 
    `app.tests.unit.test_unit_models.TenancyObjectInheritedCases` instead
    
    access.models.tenancy.TenancyObject"""

    item = None



class TenancyObjectTest(
    TenancyObjectTestCases,
    TestCase,
):


    @classmethod
    def setUpTestData(self):

        class TestModel(TenancyObject):

            class Meta:

                app_label = 'access'

                verbose_name = 'Test Model'


        self.item = TestModel()



    def test_attribute_type_get_organization(self):
        """Attribute Type

        get_organization is of type str
        """


        with pytest.raises(ObjectDoesNotExist) as err:

            self.item.get_organization()


    def test_attribute_type_history_app_label(self):
        """Attribute Type

        history_app_name is of type str
        """

        assert self.model.history_app_label is None


    def test_attribute_type_history_model_name(self):
        """Attribute Type

        history_model_name is of type str
        """

        assert self.model.history_model_name is None


    def test_attribute_type_kb_model_name(self):
        """Attribute Type

        kb_model_name is of type str
        """

        assert self.model.kb_model_name is None


    def test_attribute_type_note_basename(self):
        """Attribute Type

        note_basename is of type str
        """

        assert self.model.note_basename is None


    def test_attribute_type_get_url(self):
        """Attribute Type

        This test case is an override of a test with the same name. As this
        test suite is for testing the base object, the type returned must be
        None

        get_url is of type str
        """


        with pytest.raises(NoReverseMatch) as err:

            self.item.get_url()


    def test_attribute_type_get_page_layout(self):
        """Attribute Type

        This test case is an override of a test with the same name. As this
        test suite is for testing the base object, the type returned must be
        None

        get_page_layout is of type str
        """

        assert self.item.get_page_layout() is None
