import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.model_itasset
class ITAssetRelationshipsBaseSerializerTestCases(
    SerializerTestCases
):

    itasset_serializer_fields_removed = [
        'parent_asset_model',
        'parent',
        'child_asset_model',
    ]



    @pytest.mark.parametrize(
        argnames = "removed_field",
        argvalues = itasset_serializer_fields_removed,
        ids = itasset_serializer_fields_removed,
    )
    def test_function_get_fields_itasset(self,
        removed_field, model_serializer, kwargs_api_create
    ):
        """ Test Serializer function "get_fields"

        ensure that when the viewset is sub-model `itasset` that the appropriate
        fields are removed.
        """
        class MockView:

            kwargs = {
                'model_name': 'itasset'
            }


        kwargs = kwargs_api_create

        serializer = model_serializer['model'](
            context = {
                'view': MockView()
            },
            data = kwargs
        )

        assert removed_field not in serializer.fields.fields



    itassetmodel_serializer_fields_removed = [
        'parent_asset_model',
        'parent',
        'child',
    ]



    @pytest.mark.parametrize(
        argnames = "removed_field",
        argvalues = itassetmodel_serializer_fields_removed,
        ids = itassetmodel_serializer_fields_removed,
    )
    def test_function_get_fields_itassetmodel(self,
        removed_field, model_serializer, kwargs_api_create
    ):
        """ Test Serializer function "get_fields"

        ensure that when the viewset is sub-model `itassetmodel` that the appropriate
        fields are removed.
        """
        class MockView:

            kwargs = {
                'model_name': 'itassetmodel'
            }


        kwargs = kwargs_api_create

        serializer = model_serializer['model'](
            context = {
                'view': MockView()
            },
            data = kwargs
        )

        assert removed_field not in serializer.fields.fields



    def test_serializer_function_validate_adds_field_parent_asset_model_id(self,
        model, kwargs_api_create, model_serializer
    ):
        """Test Serializer Function
        
        When view model is `itassetmodel` the validate function must add `parent_asset_model_id`
        to the fields using the value from `view.kwargs.model_id`
        """

        kwargs = kwargs_api_create

        class MockView:

            action = 'create'

            kwargs = {
                'model_name': 'itassetmodel',
                'model_id': kwargs_api_create['parent_asset_model']
            }


        kwargs = kwargs_api_create

        del kwargs_api_create['parent_asset_model']

        serializer = model_serializer['model'](
            context = {
                'view': MockView()
            },
            data = kwargs
        )

        serializer.is_valid()

        assert serializer.validated_data.get('parent_asset_model_id', None) == MockView.kwargs['model_id']



class ITAssetRelationshipsSerializerInheritedCases(
    ITAssetRelationshipsBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetRelationshipsSerializerPyTest(
    ITAssetRelationshipsBaseSerializerTestCases
):
    pass