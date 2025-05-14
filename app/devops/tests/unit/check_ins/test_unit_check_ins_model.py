from django.test import TestCase

from access.models.tenant import Tenant as Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from devops.models.check_ins import CheckIn

from itam.models.software import Software



class Model(
    TenancyObjectInheritedCases,
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

        self.organization = Organization.objects.create(name='test_org')


        self.kwargs_item_create = {
            'software': Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            'version': '1.0',
            'deployment_id': 'desc',
            'feature': 'feature_flag',
        }

        super().setUpTestData()



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



    def test_attribute_type_app_namespace(self):
        """Attribute Type

        app_namespace is of type str
        """

        assert type(self.model.app_namespace) is str


    def test_attribute_value_app_namespace(self):
        """Attribute Type

        app_namespace has been set, override this test case with the value
        of attribute `app_namespace`
        """

        assert self.model.app_namespace == 'devops'
