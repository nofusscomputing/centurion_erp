import django
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itam.models.operating_system import OperatingSystem, OperatingSystemVersion

from settings.models.app_settings import AppSettings

User = django.contrib.auth.get_user_model()



@pytest.mark.model_operatingsystemversion
class ViewSetBase:

    model = OperatingSystemVersion

    app_namespace = 'v2'
    
    url_name = '_api_operatingsystemversion'

    change_data = {'name': '22'}

    delete_data = {}

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

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization



        os = OperatingSystem.objects.create(
            organization = self.organization,
            name = 'one-add'
        )



        self.global_organization = Organization.objects.create(
            name = 'test_global_organization'
        )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = '22',
            operating_system = os
        )

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = self.global_organization

        app_settings.save()








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


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        os_b = OperatingSystem.objects.create(
            organization = different_organization,
            name = 'two-add'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = '5',
            operating_system = os
        )

        self.other_org_item = self.model.objects.create(
            organization = different_organization,
            name = '6',
            operating_system = os_b
        )


        self.url_view_kwargs = {'operating_system_id': os.id, 'pk': self.item.id}

        self.url_kwargs = {'operating_system_id': os.id,}

        self.add_data = {
            'name': '22',
            'organization': self.organization.id,
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
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



@pytest.mark.module_itam
class OperatingSystemVersionMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
