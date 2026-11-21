import pytest

from datetime import datetime, timedelta

from django.core.exceptions import (
    ValidationError
)
from django.db import models
from django.utils.timezone import make_aware

from accounting.tests.unit.asset_base.test_unit_asset_base_model import (
    AssetBaseModelInheritedCases,
    AssetBase
)

from itam.models import ITAsset
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_model  import (
    ITAMAssetModelInheritedCases
)



@pytest.mark.model_itasset
class ITAssetModelTestCases(
    ITAMAssetModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            'app_namespace': {
                'type': str,
                'value': 'accounting'
            },
            'model_tag': {
                'type': str,
                'value': 'device'
            },
            'url_model_name': {
                'type': str,
                'value': 'asset'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': False,
            'unique': True,
        },
        'uuid': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.UUIDField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'imei': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'mac_address': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'puk': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'puk_pin': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'device_model': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'config': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'inventorydate': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'is_virtual': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        }
    }


    def test_class_inherits_itasset(self, model):
        """ Class inheritence

        Model Must Inherit from itasset
        """

        assert issubclass(model, ITAsset)



    def test_function_clean_fields_calls_clean_fields_asset_model(self, mocker,
        model, model_kwargs
    ):
        """Class Function check
        
        Ensure that as part of clean_fields being called, the device_model
        mandatory fields are also checked. i.e. `clean_fields_asset_model` called
        """

        kwargs = model_kwargs()

        the_model = model(**kwargs)

        mocked_field = mocker.patch.object(the_model, 'clean_fields_asset_model', return_value = True)

        the_model.clean_fields()

        mocked_field.assert_called()



    mandatory_model_fields_from_type = [
        'imei',
        'mac_address',
        'puk',
        'puk_pin',
        'serial_number',
    ]



    @pytest.mark.parametrize(
        argnames = "mandatory_field",
        argvalues = mandatory_model_fields_from_type,
        ids = mandatory_model_fields_from_type,
    )
    def test_function_clean_fields_asset_model_checks_required_field(self, mocker,
        model, model_kwargs, mandatory_field
    ):
        """Class Function check
        
        Ensure that as part of checking required the correct fields are called.
        """

        kwargs = model_kwargs()

        the_model = model(**kwargs)

        mocked_field = mocker.patch.object(
            type(the_model.device_model),
            mandatory_field,
            new_callable=mocker.PropertyMock,
            return_value=True,
        )

        the_model.clean_fields_asset_model()

        mocked_field.assert_called()



    @pytest.mark.parametrize(
        argnames = "mandatory_field",
        argvalues = mandatory_model_fields_from_type,
        ids = mandatory_model_fields_from_type,
    )
    def test_function_clean_fields_asset_model_validates_field(self, mocker,
        model, model_kwargs, mandatory_field
    ):
        """Class Function check
        
        Ensure that as part of checking required if the field is not populated
        raise a validation exception.
        """

        kwargs = model_kwargs()

        del kwargs[mandatory_field]

        the_model = model(**kwargs)

        mocked_field = mocker.patch.object(
            type(the_model.device_model),
            mandatory_field,
            new_callable=mocker.PropertyMock,
            return_value=True,
        )

        with pytest.raises(ValidationError) as exc:

            the_model.clean_fields_asset_model()



    @pytest.mark.parametrize(
        argnames = "mandatory_field",
        argvalues = mandatory_model_fields_from_type,
        ids = mandatory_model_fields_from_type,
    )
    def test_function_clean_fields_asset_model_error_ouputs_msg_field(self, mocker,
        model, model_kwargs, mandatory_field
    ):
        """Class Function check
        
        Ensure that as part of checking required if the field is not populated
        raises a validation exception with the required msg.
        """

        kwargs = model_kwargs()

        del kwargs[mandatory_field]

        the_model = model(**kwargs)

        mocked_field = mocker.patch.object(
            type(the_model.device_model),
            mandatory_field,
            new_callable=mocker.PropertyMock,
            return_value=True,
        )

        with pytest.raises(ValidationError) as exc:

            the_model.clean_fields_asset_model()

        assert exc.value.args[1] == 'required'



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model has its own stringify convention' )
    def test_function__str__has_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if asset_number exists that it is used in model
        stringify.
        """

        test_model = model( **model_kwargs() )

        assert str(test_model).endswith(test_model.asset_number)



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'model has its own stringify convention' )
    def test_function__str__no_asset_number(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if there is not asset_number that it is not used in model
        stringify.
        """

        kwargs = model_kwargs()
        del kwargs['asset_number']

        test_model = model( **kwargs )

        assert test_model._meta.verbose_name == str(test_model)



    def test_function_validate_config_keys_not_reserved_software(self, model):
        """Test model function
        
        ensure that a config key in reserved list of config keys raises an
        exception.
        """

        with pytest.raises(ValidationError):

            model.validate_config_keys_not_reserved({'software': ['a']})



    def test_function_validate_config_validate_config_keys_is_dict(self, model):
        """Test model function
        
        ensure that a config key passed as dict does not raise exception.
        """

        assert model.validate_config_keys_is_dict({'software': ['a']}) == None



    def test_function_validate_config_validate_config_keys_is_dict_str(self, model):
        """Test model function
        
        ensure that a config key passed as str raises a validation exception.
        """

        with pytest.raises(ValidationError):

            model.validate_config_keys_is_dict("{'software': ['a']}")



    def test_property_status_no_date(self, model, model_kwargs):
        """ Test model property

        Ensure that status returns `UKN` when no inventory date has been
        supplied.
        """

        test_obj = model( **model_kwargs() )

        test_obj.inventorydate = None

        assert test_obj.status == 'UNK'



    def test_property_status_ok(self, model, model_kwargs):
        """ Test model property

        Ensure that status returns `ok` when the checkdate < 1 days
        """

        test_obj = model( **model_kwargs() )

        test_obj.inventorydate = make_aware(datetime.now()) - timedelta( days = 1 )

        assert test_obj.status == 'OK'



    def test_property_status_warn(self, model, model_kwargs):
        """ Test model property

        Ensure that status returns `warn` when the checkdate < 2 days
        """

        test_obj = model( **model_kwargs() )

        test_obj.inventorydate = make_aware(datetime.now()) - timedelta( days = 2 )

        assert test_obj.status == 'WARN'



    def test_property_status_bad(self, model, model_kwargs):
        """ Test model property

        Ensure that status returns `bad` when the checkdate < 3 days
        """

        test_obj = model( **model_kwargs() )

        test_obj.inventorydate = make_aware(datetime.now()) - timedelta( days = 3 )

        assert test_obj.status == 'BAD'



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass
