import django
import pytest

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from access.models.tenant import Tenant as Organization

from centurion.tests.abstract.mock_view import MockView

from devops.serializers.software_enable_feature_flag import SoftwareEnableFeatureFlag, ModelSerializer

from itam.models.software import Software

User = django.contrib.auth.get_user_model()



class ValidationAPI(
    TestCase,
):

    model = SoftwareEnableFeatureFlag

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an org
        2. Create an item
        """

        organization = Organization.objects.create(name='test_org')

        self.other_organization = Organization.objects.create(name='test_org_other')

        self.organization = organization

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.valid_data = {
            'organization': self.organization.id,
            # 'name': 'two',
            'software': software.id,
            # 'description': 'a description',
            # 'model_notes': 'dfsdfsd',
            'enabled': True
        }

        
        self.user = User.objects.create(
            username = 'user',
            password = 'password',
            is_superuser = True,
        )

        self.mock_view = MockView(
            model = self.model,
            user = self.user,
        )

        self.mock_view.kwargs = {
            'software_id': software.id
        }





    def test_serializer_validation_valid_data(self):
        """Serializer Validation Check

        Ensure that if creating and no name is provided a validation error occurs
        """

        serializer = ModelSerializer(
            context = {
                'view': self.mock_view,
                'request': self.mock_view.request
            },
            data = self.valid_data
        )


        assert serializer.is_valid( raise_exception = True )


    def test_serializer_validation_no_organization_exception(self):
        """Serializer Validation Check

        Ensure that when creating and field organization is not provided a
        validation error occurs
        """

        valid_data = self.valid_data.copy()

        del valid_data['organization']

        with pytest.raises(ValidationError) as err:

            serializer = ModelSerializer(
                context = {
                    'view': self.mock_view,
                    'request': self.mock_view.request
                },
                data = valid_data
            )

            serializer.is_valid(raise_exception = True)
            serializer.save()

        assert err.value.get_codes()['organization'] == 'required'
