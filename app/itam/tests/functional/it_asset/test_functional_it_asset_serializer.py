import pytest

from accounting.tests.functional.asset_base.test_functional_asset_base_serializer import (
    MockView
)

from itam.tests.functional.itamasset_base.test_functional_itamasset_base_serializer import (
    ITAMAssetBaseSerializerInheritedCases
)



@pytest.mark.model_itasset
class ITAssetSerializerTestCases(
    ITAMAssetBaseSerializerInheritedCases
):


    parameterized_test_data: dict = {}

    valid_data: dict = {
        'name': 'asdsa',
        'asset_number': 'abc',
        'serial_number': 'def',
        'model_notes': 'sdasds',
    }


    dynamic_mandatory_fields = [
        ( 'metadata', 'imei' ),
        ( 'metadata', 'mac_address' ),
        ( 'metadata', 'puk' ),
        ( 'metadata', 'puk_pin' ),
        ( 'metadata', 'serial_number' ),
    ]


    @pytest.mark.parametrize(
        argnames = "view_action, field_name",
        argvalues = dynamic_mandatory_fields,
        ids = [
            f'{view_action}_{field_name}'
                for view_action, field_name in dynamic_mandatory_fields
        ],
    )
    def test_serializer_metadata_asset_model_dynamic_mandatory_field_allow_blank(self,
        create_serializer, model, model_kwargs,
        view_action, field_name,
    ):
        """Dynamic Field Update Check

        When a metadata request is made the field needs to be marked as
        `allow_blank = False` so that the UI can mark the HTML field as required,
        """

        valid_data = self.valid_data.copy()

        asset = model.objects.create( **model_kwargs() )

        view_set = MockView()

        view_set.action = view_action

        view_set.kwargs = {}

        view_set.kwargs['pk'] = asset.pk

        serializer = create_serializer(
            context = {
                'view': view_set,
            },
            data = valid_data
        )

        assert getattr(asset.device_model, field_name, '-') == True, \
            'Test cant continue if model field is not true.'

        assert serializer.fields[field_name].allow_blank == False



    @pytest.mark.parametrize(
        argnames = "view_action, field_name",
        argvalues = dynamic_mandatory_fields,
        ids = [
            f'{view_action}_{field_name}'
                for view_action, field_name in dynamic_mandatory_fields
        ],
    )
    def test_serializer_metadata_asset_model_dynamic_mandatory_field_required(self,
        create_serializer, model, model_kwargs,
        view_action, field_name,
    ):
        """Dynamic Field Update Check

        When a metadata request is made the field needs to be marked as
        `required = True` so that the UI can mark the HTML field as required,
        """

        valid_data = self.valid_data.copy()

        asset = model.objects.create( **model_kwargs() )

        view_set = MockView()

        view_set.action = view_action

        view_set.kwargs = {}

        view_set.kwargs['pk'] = asset.pk

        serializer = create_serializer(
            context = {
                'view': view_set,
            },
            data = valid_data
        )

        assert getattr(asset.device_model, field_name, '-') == True, \
            'Test cant continue if model field is not true.'

        assert serializer.fields[field_name].required == True




class ITAssetSerializerInheritedCases(
    ITAssetSerializerTestCases,
):

    parameterized_test_data: dict = None

    create_model_serializer = None
    """Serializer to test"""

    model = None
    """Model to test"""

    valid_data: dict = None
    """Valid data used by serializer to create object"""



@pytest.mark.module_itam
class ITAssetSerializerPyTest(
    ITAssetSerializerTestCases,
):

    pass
