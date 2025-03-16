from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from devops.models.check_ins import CheckIn

from itam.models.software import Software



class Model(
    TenancyModel,
    TestCase,
):

    model = CheckIn

    should_model_history_be_saved: bool = False


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization


        self.item = self.model.objects.create(
            organization = self.organization,
            software = Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            version = '1.0',
            deployment_id = 'desc',
            feature = 'feature_flag',
        )


    def test_attribute_not_empty_get_url(self):
        """Test field `<model>` is not empty

        This test case is a duplicate of a test with the smae name. As this
        model does not require this attribute, this test is N/A.

        Attribute `get_url` must contain values
        """

        pass


    def test_attribute_type_get_url(self):
        """Test field `<model>`type

        This test case is a duplicate of a test with the smae name. As this
        model does not require this attribute, this test is N/A.

        Attribute `get_url` must be str
        """

        pass
