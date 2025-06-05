import inspect
import pytest

from django.db import models
from django.core.exceptions import (
    ValidationError
)
from django.utils.timezone import now

from access.tests.unit.tenancy_abstract.test_unit_tenancy_abstract_model import (
    TenancyAbstractModelInheritedCases
)

from core.models.centurion import CenturionModel




@pytest.mark.centurion_models
class CenturionAbstractModelTestCases(
    TenancyAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):
        
        return {
            '_audit_enabled': {
                'type': bool,
                'value': True,
            },
            '_is_submodel': {
                'type': bool,
                'value': False,
            },
            '_notes_enabled': {
                'type': bool,
                'value': True,
            },
            'model_tag': {
                'type': str,
            },
            'url_model_name': {
                'type': type(None),
                'value': None,
            }
        }

    @property
    def parameterized_model_fields(self):
        
        return {
            'id': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.IntegerField,
                'null': False,
                'unique': True,
            },
            'model_notes': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            'created': {
                'blank': False,
                'default': now,
                'field_type': models.IntegerField,
                'null': False,
                'unique': False,
            },
        }



    def test_class_inherits_centurion_model(self, model):
        """ Class Check

        Ensure this model inherits from `CenturionModel`
        """

        assert issubclass(model, CenturionModel)



    def test_method_centurion_delete_called(self, mocker, model_instance):
        """Test Class Method

        Ensure method `core.models.centurion.CenturionModel.delete()` is called
        when `model.delete()` is called.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        mocker.patch('django.db.models.base.Model.delete', return_value = None)

        delete = mocker.patch('core.models.centurion.CenturionModel.delete', return_value = None)

        model_instance.delete()

        delete.assert_called_once()



    def test_method_centurion_save_called(self, mocker, model_instance):
        """Test Class Method

        Ensure method `core.models.centurion.CenturionModel.save()` is called
        when `model.save()` is called.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        save = mocker.patch('core.models.centurion.CenturionModel.save', return_value = None)

        model_instance.save()

        save.assert_called_once()



    def test_method_delete_calls_super_keep_parent_matches_is_sub_model(self, mocker, model_instance):
        """Test Class Method
        
        Ensure when method `delete` calls `super().delete` attribute
        `keep_parents` is the same value as `model._is_submodel`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

            # def get_queryset(self):
            #     return model_instance


        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)
        # mocker.patch('access.models.tenancy_abstract.TenancyManager', new_callable=MockManager)
        # mocker.patch('access.models.tenancy.TenancyManager', new_callable=MockManager)

    
        super_delete = mocker.patch('django.db.models.base.Model.delete', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = {'key': 'value'})

        model_instance.delete()


        super_delete.assert_called_with(using = None, keep_parents = model_instance._is_submodel)



    def test_method_get_history_model_name_returns__AuditModelName(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_history_model_name` returns the value of the models
        audit name `<Model Class name>AuditHistory`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        test_value = f'{model_instance._meta.object_name}AuditHistory'


        assert model_instance.get_history_model_name() == test_value



    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        model_instance.id = 1

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == { 'pk': model_instance.id }



    def test_method_validate_field_not_none_raises_exception(self, model):
        """ Test Class Method

        Ensure that method `validate_field_not_none` raises a validation error
        when it's passed a value of `None`
        """

        with pytest.raises(ValidationError) as e:

            model.validate_field_not_none(None)

        assert e.value.code == 'field_value_not_none'



    def test_method_validate_field_not_none_no_exception(self, model):
        """ Test Class Method

        Ensure that method `validate_field_not_none` does not raise an
        exception when the value is not `None`.
        """

        assert model.validate_field_not_none('a value') == None



class CenturionAbstractModelInheritedCases(
    CenturionAbstractModelTestCases,
):


    parameterized_class_attributes = {
        'page_layout': {
            'type': list,
        },
        'table_fields': {
            'type': list,
        }
    }


    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None



class CenturionAbstractModelPyTest(
    CenturionAbstractModelTestCases,
):

    @property
    def parameterized_class_attributes(self):
        
        return {
            'model_tag': {
                'type': type(None),
                'value': None,
            },
            'url_model_name': {
                'type': type(None),
            }
        }



    def test_model_is_abstract(self, model):

        assert model._meta.abstract



    def test_method_clean_calls_super_clean(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch('django.db.models.base.Model.clean', return_value = None)

        model_instance.clean()


        super_clean.assert_called_once()



    def test_method_clean_fields_calls_super_clean_fields(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean_fields` calls `super().clean_fields`
        """

        super_clean_fields = mocker.patch('django.db.models.base.Model.clean_fields', return_value = None)

        model_instance.clean_fields()

        super_clean_fields.assert_called_once()



    def test_method_delete_audit_disabled_no_data_collected(self, mocker, model_instance):
        """Test Class Method

        Ensure method `delete` does not call `self.get_audit_values` when
        auditing is disabled.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = False

        mocker.patch('django.db.models.base.Model.delete', return_value = None)

        get_audit_values = mocker.spy(CenturionModel, 'get_audit_values')

        model_instance.delete()


        get_audit_values.assert_not_called()



    def test_method_delete_audit_enabled_data_collected(self, mocker, model_instance):
        """Test Class Method

        Ensure method `delete` calls `self.get_audit_values` when auditing
        is enabled.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        model_instance._audit_enabled = True

        mocker.patch('django.db.models.base.Model.delete', return_value = None)

        get_audit_values = mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = {'key': 'value'})

        model_instance.delete()


        get_audit_values.assert_called_once()



    def test_method_delete_default_attributes(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `delete`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.delete)

        default_keep_parents = sig.parameters['keep_parents'].default
        using = sig.parameters['using'].default

        assert(
            default_keep_parents is None
            and using is None
        )



    def test_method_delete_calls_super_is_sub_model(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `delete` calls `super().delete` with correct parameters
        when model is not a sub-model
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        model_instance._is_submodel = True

        super_delete = mocker.patch('django.db.models.base.Model.delete', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = {'key': 'value'})

        model_instance.delete()


        super_delete.assert_called_with(using = None, keep_parents = True)



    def test_method_delete_calls_super_not_sub_model(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `delete` calls `super().delete` with correct parameters
        when model is not a sub-model
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        model_instance._is_submodel = False

        super_delete = mocker.patch('django.db.models.base.Model.delete', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = {'key': 'value'})

        model_instance.delete()


        super_delete.assert_called_with(using = None, keep_parents = False)



    def test_method_delete_is_called_get_audit_values(self, mocker, model_instance):
        """Test Class Method

        Ensure that if `model.get_audit_values = True`, method
        `self.get_audit_values()` is called.

        In the alternate, if `model.get_audit_values = False` method
        `self.get_audit_values()` must not be called.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        super_delete = mocker.patch('django.db.models.base.Model.delete', return_value = None)

        get_audit_values = mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = {'key': 'value'})

        model_instance.delete()

        if model_instance._audit_enabled:

            get_audit_values.assert_called_once()

        else:

            get_audit_values.assert_not_called()



    def test_method_full_clean_default_attributes(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` has the defined default attributes.
        """

        sig = inspect.signature(model_instance.full_clean)

        exclude = sig.parameters['exclude'].default
        validate_unique = sig.parameters['validate_unique'].default
        validate_constraints = sig.parameters['validate_constraints'].default

        assert(
            exclude is None
            and validate_unique is True
            and validate_constraints is True
        )


    def test_method_full_clean_calls_super_full_clean(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` calls `super().full_clean` with specified
        parameters.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        super_full_clean = mocker.patch('django.db.models.base.Model.full_clean', return_value = None)

        model_instance.full_clean()


        super_full_clean.assert_called_with(
            exclude = None,
            validate_unique = True,
            validate_constraints = True
        )



    def test_method_full_clean_calls_clean(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` calls `self.clean`.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        for field in self.kwargs_create_item:

            setattr(model_instance, field, self.kwargs_create_item[field])


        clean = mocker.patch('core.models.centurion.CenturionModel.clean', return_value = None)

        model_instance.full_clean()


        clean.assert_called_once()


    
    def test_method_full_clean_calls_clean_fields(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` calls `self.clean_fields()`.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        for field in self.kwargs_create_item:

            setattr(model_instance, field, self.kwargs_create_item[field])


        clean_fields = mocker.patch('core.models.centurion.CenturionModel.clean_fields', return_value = None)

        model_instance.full_clean()


        clean_fields.assert_called_once()



    def test_method_full_clean_calls_validate_constraints(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` calls `self.validate_constraints()`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        for field in self.kwargs_create_item:

            setattr(model_instance, field, self.kwargs_create_item[field])


        validate_constraints = mocker.patch('core.models.centurion.CenturionModel.validate_constraints', return_value = None)

        model_instance.full_clean()


        validate_constraints.assert_called_once()



    def test_method_full_clean_calls_validate_unique(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `full_clean` calls `self.validate_unique()`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        for field in self.kwargs_create_item:

            setattr(model_instance, field, self.kwargs_create_item[field])


        validate_unique = mocker.patch('core.models.centurion.CenturionModel.validate_unique', return_value = None)

        model_instance.full_clean()


        validate_unique.assert_called_once()



    def test_method_get_audit_values_clean_model_returns_empty_dict(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_audit_values` returns an empty dict if `id = None`.
        (is an empty model)
        """

        for field, value in self.kwargs_create_item.items():

            setattr(model_instance, field, value)

        class MockManager:

            def get(*args, **kwargs):
                return model_instance


        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        assert model_instance.get_audit_values() == {
            'id': None,
            **self.kwargs_create_item
        }



    def test_method_get_audit_values_clean_model_returns_fields_only(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_audit_values` returns All model fields as a dict
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance.id = 1

        for field in self.kwargs_create_item:

            setattr(model_instance, field, self.kwargs_create_item[field])

        method_values = model_instance.get_audit_values()

        assert method_values == {
            'id': model_instance.id,
            **self.kwargs_create_item,
        }    # Correct Values Returned

        assert len(method_values) == len(model_instance._meta.fields)    # Fail-Safe to ensure test writer fills all fields



    def test_method_get_after_returns__after(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_after` returns the value of `model._after`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        test_value = {
            'key_after': 'value_after'
        }

        model_instance._after = test_value

        assert model_instance.get_after() == test_value



    def test_method_get_before_returns__before(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_after` returns the value of `model._before`
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        test_value = {
            'key_before': 'value_before'
        }

        model_instance._before = test_value

        assert model_instance.get_before() == test_value



    def test_method_get_url_default_attributes(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_url`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.get_url)

        relative = sig.parameters['relative'].default
        api_version = sig.parameters['api_version'].default

        assert(
            relative == False
            and api_version == 2
        )



    def test_method_get_url_called_reverse(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = 'None')

        model_instance.id = 1
        url_basename = f'v2:_api_{model_instance._meta.model_name}-detail'

        url = model_instance.get_url()

        reverse.assert_called_with( url_basename, None, { 'pk': model_instance.id }, None, None )



    def test_method_get_url_returned_non_relative(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        settings.SITE_URL = 'https://domain.tld'

        site_path = '/module/page/1'

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        test_value = settings.SITE_URL + site_path

        model_instance.id = 1

        url = model_instance.get_url( relative = False)

        assert url == test_value



    def test_method_get_url_returned_relative(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        model_instance.id = 1

        url = model_instance.get_url( relative = True)

        assert url == site_path



    def test_method_get_url_attribute_url_model_name_set(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url` calls reverse
        """

        site_path = '/module/page/1'

        reverse = mocker.patch('rest_framework.reverse._reverse', return_value = site_path)

        model_instance.id = 1
        model_instance.url_model_name = 'testmodel'

        url_basename = f'v2:_api_testmodel-detail'

        url = model_instance.get_url( relative = True)

        model_instance.url_model_name = None    # Reset Val

        reverse.assert_called_with( url_basename, None, { 'pk': model_instance.id }, None, None )



    def test_method_save_audit_enabled_sets__after_create_model(self, mocker, model_user, model_instance):
        """Test Class Method
        
        Ensure method `save` sets attribute `self._after` to the value of the
        `self.get_audit_values()`.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = True

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        user = model_user.objects.create(
            username = 'centurion_abstract',
            password = 'password'
        )

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.context', return_value = {
            'user': user,
            'logger': None
        })

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        test_value = {
            'save_before_key': 'save_before_value'
        }

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = test_value)

        model_instance.save()

        assert model_instance._after == test_value



    def test_method_save_audit_enabled_sets__before_create_model(self, mocker, model_user, model_instance):
        """Test Class Method
        
        Ensure method `save` sets attribute `self._before` with an empty dict for new model
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = True

        user = model_user.objects.create(
            username = 'centurion_abstract',
            password = 'password'
        )

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.context', return_value = {
            'user': user,
            'logger': None
        })

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = None)

        model_instance.save()

        assert model_instance._before == {}



    def test_method_save_audit_enabled_sets__after_update_model(self, mocker, model_user, model_instance):
        """Test Class Method
        
        Ensure method `save` sets attribute `self._after` to the value of the
        `self.get_audit_values()`.
        """

        class MockManager:

            class MockObj:

                def get_audit_values(self):
                    return {}

            def get(self, *args, **kwargs):
                return self.MockObj()

        user = model_user.objects.create(
            username = 'centurion_abstract',
            password = 'password'
        )

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.context', return_value = {
            'user': user,
            'logger': None
        })

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        model_instance.id = 1

        model_instance._audit_enabled = True

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        test_value = {
            'save_before_key': 'save_before_value'
        }

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = test_value)

        model_instance.save()

        assert model_instance._after == test_value



    def test_method_save_audit_enabled_sets__before_update_model(self, mocker, model_user, model_instance):
        """Test Class Method
        
        Ensure method `save` sets attribute `self._before` to field values
        before using method `model.get_audit_values()`.
        """

        test_value = {
            'save_before_key': 'save_before_value'
        }

        class MockManager:

            class MockObj:

                def get_audit_values(self):
                    return test_value

            def get(self, *args, **kwargs):
                return self.MockObj()

        user = model_user.objects.create(
            username = 'centurion_abstract',
            password = 'password'
        )

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.context', return_value = {
            'user': user,
            'logger': None
        })

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.objects', new_callable=MockManager)

        model_instance.id = 1

        model_instance._audit_enabled = True

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = None)

        model_instance.save()

        assert model_instance._before == test_value



    def test_method_save_default_attributes(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_url`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.save)

        force_insert = sig.parameters['force_insert'].default
        force_update = sig.parameters['force_update'].default
        using = sig.parameters['using'].default
        update_fields = sig.parameters['update_fields'].default

        assert(
            force_insert == False
            and force_update == False
            and using == None
            and update_fields == None
        )



    def test_method_save_calls_full_clean(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `save` calls `self.full_clean` with the defined attributes.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = False

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        full_clean = mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        model_instance.save()

        full_clean.assert_called_with(
            exclude = None,
            validate_unique = True,
            validate_constraints = True
        )



    def test_method_save_calls_super_save(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `save` calls `super().save` with the defined attributes.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = False

        super_save = mocker.patch('django.db.models.base.Model.save', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        model_instance.save()


        super_save.assert_called_with(
            force_insert = False,
            force_update = False,
            using = None,
            update_fields = None
        )



    def test_method_save_audit_enabled_calls_get_audit_values_create_model(self, mocker, model_user, model_instance):
        """Test Class Method
        
        Ensure method `save` calls `self.get_audit_values()` with the defined attributes.
        """

        class MockManager:

            def get(*args, **kwargs):
                return model_instance

        model_instance.objects = MockManager()

        model_instance._audit_enabled = True

        user = model_user.objects.create(
            username = 'centurion_abstract',
            password = 'password'
        )

        mocker.patch('access.models.tenancy_abstract.TenancyAbstractModel.context', return_value = {
            'user': user,
            'logger': None
        })

        mocker.patch('django.db.models.base.Model.save', return_value = None)

        mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        get_audit_values = mocker.patch('core.models.centurion.CenturionModel.get_audit_values', return_value = None)

        model_instance.save()

        get_audit_values.assert_called_with()



    def test_method_validate_constraints_calls_super_validate_constraints(self, mocker, model_instance):
        """Test Class Method

        Ensure method `validate_constraints` calls `super().validate_constraints`
        """

        super_validate_constraints = mocker.patch('django.db.models.base.Model.validate_constraints', return_value = None)

        model_instance.validate_constraints()


        super_validate_constraints.assert_called_once()



    def test_method_validate_unique_fields_calls_super_validate_unique(self, mocker, model_instance):
        """Test Class Method

        Ensure method `validate_unique` calls `super().validate_unique`
        """

        super_validate_unique = mocker.patch('django.db.models.base.Model.validate_unique', return_value = None)

        model_instance.validate_unique()

        super_validate_unique.assert_called_once()
