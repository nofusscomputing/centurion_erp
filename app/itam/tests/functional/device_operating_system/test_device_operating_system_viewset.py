import django
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases
from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from itam.serializers.device_operating_system import Device, DeviceOperatingSystem, DeviceOperatingSystemModelSerializer
from itam.models.operating_system import OperatingSystem, OperatingSystemVersion

User = django.contrib.auth.get_user_model()



class ViewSetBase:

    model = DeviceOperatingSystem

    app_namespace = 'v2'
    
    url_name = '_api_v2_device_operating_system'

    change_data = {'name': '1.1'}

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

        # device = Device.objects.create(
        #     organization = self.organization,
        #     name = 'a-device'
        # )

        # software = Software.objects.create(
        #     organization = self.organization,
        #     name = 'a-software'
        # )

        # software_b = Software.objects.create(
        #     organization = self.organization,
        #     name = 'b-software'
        # )


        # self.item = self.model.objects.create(
        #     organization = self.organization,
        #     device = device,
        #     software = software
        # )


        self.operating_system = OperatingSystem.objects.create(
            organization=organization,
            name = '12',
        )

        self.operating_system_version = OperatingSystemVersion.objects.create(
            organization=organization,
            name = '12',
            operating_system = self.operating_system
        )

        self.device = Device.objects.create(
            organization=organization,
            name = 'device'
        )

        self.device_two = Device.objects.create(
            organization=organization,
            name = 'device-two'
        )

        self.device_three = Device.objects.create(
            organization=different_organization,
            name = 'device-three'
        )


        self.item = self.model.objects.create(
            organization=self.organization,
            version = '1',
            operating_system_version = self.operating_system_version,
            device = self.device
        )

        self.other_org_item = self.model.objects.create(
            organization=different_organization,
            version = '1',
            operating_system_version = self.operating_system_version,
            device = self.device_three
        )


        self.url_view_kwargs = {'device_id': self.device.id, 'pk': self.item.id}

        self.url_kwargs = {'device_id': self.device_two.id}

        self.add_data = {
            'organization': self.organization.pk,
            'version': '2',
            'operating_system_version': self.operating_system_version.pk,
            'device': self.device_two.pk,
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



class DeviceOperatingSystemPermissionsAPI(
    ViewSetBase,
    APIPermissions,
    TestCase,
):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



class DeviceOperatingViewSet(
    ViewSetBase,
    SerializersTestCases,
    TestCase
):

    pass



class DeviceOperatingMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
