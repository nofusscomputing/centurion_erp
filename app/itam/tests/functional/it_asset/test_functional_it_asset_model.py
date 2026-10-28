import pytest

from django.core.exceptions import ValidationError

from itam.tests.functional.itamasset_base.test_functional_itam_asset_base_model import (
    ITAMAssetBaseModelInheritedCases
)



@pytest.mark.model_itasset
class ITAssetModelTestCases(
    ITAMAssetBaseModelInheritedCases
):


    def test_field_validation_invalid_name_starts_with_digit(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid name 'starts with digit'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['name'] = '9dev-name'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['name'][0].code == 'invalid_hostname'



    def test_field_validation_invalid_name_contains_hyphon(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid name 'contains hyphon'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['name'] = 'has_a_hyphon'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['name'][0].code == 'invalid_hostname'



    def test_field_validation_invalid_name_ends_with_dash(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid name 'ends with dash'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['name'] = 'ends-with-dash-'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['name'][0].code == 'invalid_hostname'



    def test_field_validation_invalid_mac_address(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is provided in wrong format a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'a0-b1-c2-d3-e4-f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_first_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'z0:b1:c2:d3:e4:f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_first_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'z0:b1:c2:d3:e4:f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_third_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'a0:b1:z2:d3:e4:f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_fourth_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'a0:b1:c2:z3:e4:f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_fifth_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'a0:b1:c2:d3:z4:f5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_mac_address_sixth_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that mac address is invalid a validation error
        is raised.
        """

        kwargs = model_kwargs()
        kwargs['mac_address'] = 'a0:b1:c2:d3:e4:z5'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['mac_address'][0].code == 'invalid_mac_address'



    def test_field_validation_invalid_uuid_first_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet not hex'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = 'g0000000-0000-0000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_first_octet_wrong_length(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'first octet wrong length'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '0000000-0000-0000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_second_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet not hex'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-g000-0000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_second_octet_wrong_length(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'second octet wrong length'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-000-0000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_third_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet not hex'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-g000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_third_octet_wrong_length(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'third octet wrong length'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-000-0000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_fourth_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet not hex'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-0000-g000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_fourth_octet_wrong_length(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'fourth octet wrong length'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-0000-000-000000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_fifth_octet(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet not hex'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-0000-0000-g00000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'



    def test_field_validation_invalid_uuid_fifth_octet_wrong_length(self,
        model, model_kwargs
    ):
        """Model Field Validation Check

        Ensure that if an existing item is given an invalid uuid 'fifth octet wrong length'
        it raises a validation error
        """

        kwargs = model_kwargs()
        kwargs['uuid'] = '00000000-0000-0000-0000-00000000000'

        created = model(**kwargs)

        with pytest.raises(ValidationError) as err:

            created.clean_fields()

        assert err.value.args[0]['uuid'][0].code == 'invalid'




    def test_model_create_calls_create_asset_connections(self, mocker,
        model, model_kwargs, model_itassetmodel
    ):
        """Test Model Function
        
        When an asset is created, `create_asset_connections` must be called to create connections from
        asset_model.
        """

        test_function = mocker.patch.object(
            model_itassetmodel,
            'create_asset_connections',
            return_value = ''
        )

        model.objects.create( **model_kwargs() )

        test_function.assert_called_once()



    def test_model_create_calls_create_asset_connections_args(self, mocker,
        model, model_kwargs, model_itassetmodel
    ):
        """Test Model Function
        
        When an asset is created, `create_asset_connections` is called with the
        correct kargs
        """

        test_function = mocker.patch.object(
            model_itassetmodel,
            'create_asset_connections',
            return_value = ''
        )

        parent_model = model.objects.create( **model_kwargs() )

        test_function.assert_called_once_with( parent_asset = parent_model )




    def test_model_save_no_calls_create_asset_connections(self, mocker,
        model, model_kwargs, model_itassetmodel
    ):
        """Test Model Function
        
        When an asset is created, `create_asset_connections` must be called to create connections from
        asset_model.
        """

        test_function = mocker.patch.object(
            model_itassetmodel,
            'create_asset_connections',
            return_value = ''
        )

        test_obj = model.objects.create( **model_kwargs() )

        test_function.reset_mock()

        test_obj.name = 'fred'

        test_obj.save()

        test_function.assert_not_called()



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass
