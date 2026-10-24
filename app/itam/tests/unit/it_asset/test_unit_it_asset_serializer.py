import pytest

from itam.tests.unit.itam_asset_base.test_unit_asset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itasset
class ITAssetBaseSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):


    itasset_serializer_fields_removed = [
        'imei',
        'mac_address',
        'puk',
        'puk_pin',
        'serial_number',
    ]



    @pytest.mark.parametrize(
        argnames = "removed_field",
        argvalues = itasset_serializer_fields_removed,
        ids = itasset_serializer_fields_removed,
    )
    def test_serializer_function_get_fields_removes_non_mandatory(self,
        model, model_kwargs, model_serializer, removed_field,
    ):
        """Test Serializer Function
        
        When the serializer is loaded, the fields not marked mandatory are
        to be removed from the serializer
        """

        kwargs = model_kwargs()

        created_model = model.objects.create( **kwargs )

        setattr(created_model.device_model, removed_field, False)

        created_model.device_model.save()

        class MockView:

            action = 'update'


        kwargs = {
            'name': 'an-edited-name'
        }

        serializer = model_serializer['model'](
            created_model,
            context = {
                'view': MockView()
            },
            data = kwargs,
            partial = True
        )

        serializer.is_valid()

        assert serializer.get_fields(
            ).get(removed_field, '-field_removed_correctly-') == '-field_removed_correctly-'



class ITAssetSerializerInheritedCases(
    ITAssetBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetSerializerPyTest(
    ITAssetBaseSerializerTestCases
):
    pass