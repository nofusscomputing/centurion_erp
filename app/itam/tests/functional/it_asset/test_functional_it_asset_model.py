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



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass
