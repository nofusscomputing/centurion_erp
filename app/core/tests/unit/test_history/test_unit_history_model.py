import django

from django.contrib.auth.models import ContentType
from django.test import TestCase

from access.models.tenant import Tenant as Organization

from centurion.tests.unit.test_unit_models import TenancyObjectInheritedCases

from core.models.manufacturer_history import Manufacturer
from core.models.model_history import ModelHistory

User = django.contrib.auth.get_user_model()



class ModelHistoryTestCases(
    TenancyObjectInheritedCases
):

    model = ModelHistory

    should_model_history_be_saved = True



class ModelHistoryInheritedCases(
    ModelHistoryTestCases
):

    model = None



class ModelHistoryTest(
    ModelHistoryTestCases,
    TestCase,
):

    should_model_history_be_saved = False


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

        model = Manufacturer.objects.create(
            organization=self.organization,
            name = 'man',
        )

        self.kwargs_item_create = {
            'action': self.model.Actions.ADD,
            'user': User.objects.create_user(
                username="test_user_view", password="password", is_superuser=True
            ),
            'before': {},
            'after': {},
            'content_type': ContentType.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name,
            ),
        }

        super().setUpTestData()



    def test_attribute_type_get_url(self):
        """Attribute Type

        This test case is a duplicate test of a case with the same name.
        This model does not require this attribute.

        get_url is of type str
        """

        assert not hasattr(self, 'item.get_url')


    def test_attribute_type_get_url_kwargs(self):
        """Attribute Type

        This test case is a duplicate test of a case with the same name.
        This model does not require this attribute.

        get_url_kwargs is of type dict
        """

        assert not hasattr(self, 'item.get_url_kwargs')
