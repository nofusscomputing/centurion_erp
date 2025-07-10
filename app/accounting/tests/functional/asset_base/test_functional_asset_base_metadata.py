import django
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from accounting.models.asset_base import AssetBase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

User = django.contrib.auth.get_user_model()



@pytest.mark.model_assetbase
class MetadataTestCases(
    MetadataAttributesFunctional,
):

    add_data: dict = {
        'asset_number': 'abc',
        'serial_number': 'def',
        'model_notes': 'sdasds',
    }

    app_namespace = 'v2'

    base_model = AssetBase
    """Base model for this sub model
    don't change or override this value
    """

    change_data = None

    delete_data = {}

    kwargs_create_item: dict = {
        'asset_number': '123',
        'serial_number': '456',
        'model_notes': 'sdasds',
    }

    kwargs_create_item_diff_org: dict = {
        'asset_number': '789',
        'serial_number': '012',
        'model_notes': 'sdasds',
    }

    model = AssetBase

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = None


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.different_organization = Organization.objects.create(name='test_different_organization')

        self.view_user = User.objects.create_user(username="test_user_view", password="password")

        self.item = self.model.objects.create(
            organization = organization,
            **self.kwargs_create_item
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            **self.kwargs_create_item_diff_org
        )


        self.url_view_kwargs.update({ 'pk': self.item.id })

        if self.add_data is not None:

            self.add_data.update({
                'organization': self.organization.id,
            })


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = self.different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )


    def test_sanity_is_asset_sub_model(self):
        """Sanity Test
        
        This test ensures that the model being tested `self.model` is a
        sub-model of `self.base_model`.
        This test is required as the same viewset is used for all sub-models
        of `AssetBase`
        """

        assert issubclass(self.model, self.base_model)



class AssetBaseMetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_name = 'accounting:_api_v2_asset_sub'


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            **self.kwargs_create_item_diff_org
        }

        self.url_kwargs = {
            'asset_model': self.model._meta.sub_model_type
        }

        self.url_view_kwargs = {
            'asset_model': self.model._meta.sub_model_type
        }

        super().setUpTestData()



@pytest.mark.module_accounting
class AssetBaseMetadataTest(
    MetadataTestCases,
    TestCase,

):

    url_name = 'accounting:_api_v2_asset'
