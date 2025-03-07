from django.contrib.auth.models import (
    Permission,
    User,
)
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase

from django.shortcuts import reverse

from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

# from devops.models.feature_flag import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software

from settings.models.app_settings import AppSettings




class ViewSetBase:

    model = SoftwareEnableFeatureFlag

    app_namespace = 'v2'
    
    url_name = '_api_v2_feature_flag_software'

    change_data = {'enabled': False}

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

        self.add_organization = Organization.objects.create(name='add_organization')





        self.global_organization = Organization.objects.create(
            name = 'test_global_organization'
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
            organization = self.add_organization,
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
        TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        # SoftwareEnableFeatureFlag.objects.create(
        #     organization = self.organization,
        #     software = software,
        #     enabled = True
        # )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            software = software,
            enabled = True
        )

        # software = Software.objects.create(
        #     organization = self.organization,
        #     name = 'soft item',
        # )

        self.item = self.model.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.url_kwargs = {
            'software_id': software.id,
        }

        self.url_view_kwargs = {
            'software_id': software.id,
            'pk': self.item.id
        }

        # software = Software.objects.create(
        #     organization = self.organization,
        #     name = 'soft other org',
        # )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            software = software,
            enabled = True
        )


        self.software_add = Software.objects.create(
            organization = self.add_organization,
            name = 'soft add',
        )

        self.add_data = {
            'enabled': True,
            'organization': self.add_organization.id,
            'software': self.software_add,
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )
        # TeamUsers.objects.create(    # Required so that user can Add (without errors with duplicate constraint)
        #     team = view_team,
        #     user = self.add_user
        # )

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



class PermissionsAPI(
    ViewSetBase,
    APIPermissions,
    TestCase,
):

    pass

    def test_add_has_permission(self):
        """ Check correct permission for add 

        This test cases is a duplicate of a test with the same name. Required
        as the kwargs are different from normal

        Attempt to add as user with permission
        """

        client = Client()
        # if self.url_kwargs:

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = {
                'software_id': self.software_add.id,
            }
        )

        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 201




class ViewSet(
    ViewSetBase,
    SerializersTestCases,
    TestCase
):

    pass



class Metadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
