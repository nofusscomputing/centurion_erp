from django.contrib.auth.models import User, ContentType
from django.test import TestCase

from access.models.organization import Organization

from app.tests.abstract.models import TenancyModel

from core.models.manufacturer_history import Manufacturer, ManufacturerHistory
from core.models.model_history import ModelHistory


class ManufacturerModel(
    TestCase,
    TenancyModel
):

    model = ModelHistory

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


        self.history_entry = ManufacturerHistory.objects.create(
            organization = self.organization,
            action = self.model.Actions.ADD,
            user = User.objects.create_user(
                username="test_user_view", password="password", is_superuser=True
            ),
            before = {},
            after = {},
            content_type = ContentType.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name,
            ),
            model = model,
        )

        self.item = ModelHistory.objects.get(
            pk = self.history_entry.pk
        )

