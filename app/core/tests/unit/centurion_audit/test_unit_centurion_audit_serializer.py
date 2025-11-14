import pytest

from rest_framework.exceptions import ValidationError

from api.tests.unit.test_unit_serializer import (
    MockView,
    SerializerTestCases,
)



@pytest.mark.model_centurionaudit
class CenturionAuditSerializerTestCases(
    SerializerTestCases
):


    @pytest.mark.regression
    def test_serializer_create_calls_model_full_clean(self,
        kwargs_api_create, mocker, model, model_serializer, request_user
    ):
        pytest.xfail( reason = 'Serializer must prevent creation of object for base model. Test is N/A.' )



    @pytest.mark.regression
    def test_serializer_create_raises_excaption(self,
        kwargs_api_create, mocker, model, model_serializer, request_user
    ):
        """ Serializer Check

        Confirm that base model serializer raises exception on create.
        """

        mock_view = MockView(
            user = request_user,
            model = model,
            action = 'create',
        )

        serializer = model_serializer['model'](
            context = {
                'request': mock_view.request,
                'view': mock_view,
            },
            data = kwargs_api_create
        )

        serializer.is_valid(raise_exception = True)

        full_clean = mocker.spy(model, 'full_clean')

        with pytest.raises(ValidationError):
            serializer.save()



class CenturionAuditSerializerInheritedCases(
    CenturionAuditSerializerTestCases
):
    pass


@pytest.mark.module_core
class CenturionAuditSerializerPyTest(
    CenturionAuditSerializerTestCases
):
    pass