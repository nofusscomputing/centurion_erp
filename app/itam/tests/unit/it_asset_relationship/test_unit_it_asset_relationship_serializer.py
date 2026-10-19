import pytest

from api.tests.unit.test_unit_serializer import (
    SerializerTestCases
)



@pytest.mark.model_itasset
class ITAssetRelationshipsBaseSerializerTestCases(
    SerializerTestCases
):

    itasset_serializer_fields_removed = [
        'name',
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



class ITAssetRelationshipsSerializerInheritedCases(
    ITAssetRelationshipsBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetRelationshipsSerializerPyTest(
    ITAssetRelationshipsBaseSerializerTestCases
):
    pass