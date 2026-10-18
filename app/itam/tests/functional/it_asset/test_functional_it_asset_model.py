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



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass
