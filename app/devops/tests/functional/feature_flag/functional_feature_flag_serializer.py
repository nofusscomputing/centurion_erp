import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.tenant import Tenant as Organization

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.serializers.feature_flag import FeatureFlag, ModelSerializer

from itam.models.software import Software



class ValidationAPI(
    TestCase,
):

    model = FeatureFlag

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.diff_organization = Organization.objects.create(name='test_org_diff_org')

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )

        self.valid_data = {
            'organization': self.organization.id,
            'name': 'two',
            'software': software.id,
            'description': 'a description',
            'model_notes': 'dfsdfsd',
            'enabled': True
        }


        self.software_no_feature_flag_enabled = Software.objects.create(
            organization = self.organization,
            name = 'soft no flagging',
        )



    def test_serializer_validation_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        serializer = ModelSerializer(
            data = self.valid_data
        )


        assert serializer.is_valid( raise_exception = True )


    def test_serializer_validation_no_name_exception(self):
        """Serializer Validation Check

        Ensure that when creating and field name is not provided a
        validation error occurs
        """

        valid_data = self.valid_data.copy()

        del valid_data['name']

        with pytest.raises(ValidationError) as err:

            serializer = ModelSerializer(
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['name'][0] == 'required'


    def test_serializer_validation_no_software_exception(self):
        """Serializer Validation Check

        Ensure that when creating and field software is not provided, no
        validation error occurs
        """

        valid_data = self.valid_data.copy()

        del valid_data['software']

        with pytest.raises(ValidationError) as err:

            serializer = ModelSerializer(
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'][0] == 'required'


    def test_serializer_validation_feature_flagging_not_enabled(self):
        """Serializer Validation Check

        Ensure that when creating and the software doesn't, have feature
        flagging enabled an exception is thrown.
        """

        valid_data = self.valid_data.copy()

        valid_data['software'] = self.software_no_feature_flag_enabled.id

        with pytest.raises(ValidationError) as err:

            serializer = ModelSerializer(
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['software'] == 'feature_flagging_disabled'


    def test_serializer_validation_feature_flagging_not_enabled_for_organization(self):
        """Serializer Validation Check

        Ensure that when creating and the software doesn't, have feature
        flagging enabled an exception is thrown.
        """

        valid_data = self.valid_data.copy()

        valid_data['organization'] = self.diff_organization.id

        with pytest.raises(ValidationError) as err:

            serializer = ModelSerializer(
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)

        assert err.value.get_codes()['organization'] == 'feature_flagging_wrong_organizaiton'



    def test_serializer_validation_no_description_ok(self):
        """Serializer Validation Check

        Ensure that when creating and field description is not provided, no
        validation error occurs
        """

        valid_data = self.valid_data.copy()

        del valid_data['description']

        serializer = ModelSerializer(
            data = valid_data
        )

        assert serializer.is_valid(raise_exception = True)


    def test_serializer_validation_no_enabled_ok_default_false(self):
        """Serializer Validation Check

        Ensure that when creating and field enabled is not provided, no
        validation error occurs and enabled is set to `false`
        """

        valid_data = self.valid_data.copy()

        del valid_data['enabled']

        serializer = ModelSerializer(
            data = valid_data
        )

        assert serializer.is_valid(raise_exception = True)

        serializer.save()

        assert serializer.instance.enabled is False
