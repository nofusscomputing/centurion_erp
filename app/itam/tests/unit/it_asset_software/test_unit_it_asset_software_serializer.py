import pytest

from api.serializers.common import CommonModelSerializer
from api.tests.unit.test_unit_serializer import (
    MockView,
    SerializerTestCases
)



@pytest.mark.model_itasset
class ITAssetSoftwareBaseSerializerTestCases(
    SerializerTestCases
):

    itasset_serializer_fields_removed = [
        'parent_asset_model',
        'parent',
    ]

    # def test_serializer_create_calls_common_validate(self,
    #     kwargs_api_create, mocker, model, model_serializer, request_user,
    # ):
    #     """ Serializer Check

    #     Confirm that when creating an object `validate()` is called.
    #     """

    #     mocker.patch.object(request_user, 'has_perm', return_value = True)

    #     mocker.patch.object(request_user, 'has_perms', return_value = True)

    #     mock_view = MockView(
    #         user = request_user,
    #         model = model,
    #         action = 'create',
    #     )

    #     mock_view.kwargs = {
    #         'model_name': 'itasset',
    #         'model_id': kwargs_api_create['it_asset']
    #     }

    #     serializer = model_serializer['model'](
    #         context = {
    #             'request': mock_view.request,
    #             'view': mock_view,
    #         },
    #         data = kwargs_api_create
    #     )

    #     full_clean = mocker.spy(CommonModelSerializer, 'validate')

    #     serializer.is_valid(raise_exception = True)

    #     serializer.save()

    #     full_clean.assert_called_once()



class ITAssetSoftwareSerializerInheritedCases(
    ITAssetSoftwareBaseSerializerTestCases
):
    pass



@pytest.mark.module_itam
class ITAssetSoftwareSerializerPyTest(
    ITAssetSoftwareBaseSerializerTestCases
):
    pass