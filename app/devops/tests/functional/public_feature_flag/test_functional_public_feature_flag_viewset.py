import django
import pytest

from datetime import datetime
from dateutil import tz

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.role import Role
from access.models.tenant import Tenant

from api.tests.abstract.api_serializer_viewset import SerializerView

from devops.models.feature_flag import FeatureFlag
from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag

from itam.models.software import Software

from settings.models.app_settings import AppSettings



@pytest.mark.model_featureflag
class ViewSetBase:

    model = FeatureFlag

    app_namespace = 'v2'
    
    url_name = 'public:devops:_api_checkin'


    @classmethod
    def presetUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        User = django.contrib.auth.get_user_model()

        self.organization = Tenant.objects.create(name='test_org')

        self.different_organization = Tenant.objects.create(name='test_different_organization')

        self.global_organization = Tenant.objects.create(name='test_global_organization')

        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")

        self.add_user = User.objects.create_user(username="test_user_add", password="password")

        self.change_user = User.objects.create_user(username="test_user_change", password="password")

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")

        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")

        self.view_user = User.objects.create_user(username="test_user_view", password="password")

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = self.global_organization

        app_settings.save()


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        self.presetUpTestData()

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

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two',
            software = software,
        )


        self.url_view_kwargs = {
            'organization_id': self.organization.id,
            'software_id': software.id,
        }

        self.software_not_enabled = Software.objects.create(
            organization = self.organization,
            name = 'soft not enabled',
        )



        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        view_group = Group.objects.create(
            name = 'view_team',
        )


        view_role = Role.objects.create(
            name = 'view_team',
            organization = self.organization,
        )

        view_role.permissions.set([view_permissions])
        view_role.groups.set([view_group])

        self.view_user.groups.set([view_group])


        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        add_group = Group.objects.create(
            name = 'add_team',
        )

        add_role = Role.objects.create(
            name = 'add_team',
            organization = self.organization,
        )

        add_role.permissions.set([add_permissions])
        add_role.groups.set([add_group])

        self.add_user.groups.set([add_group])


        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        change_group = Group.objects.create(
            name = 'change_team',
        )

        change_role = Role.objects.create(
            name = 'change_team',
            organization = self.organization,
        )

        change_role.permissions.set([change_permissions])
        change_role.groups.set([change_group])

        self.change_user.groups.set([change_group])


        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )


        delete_group = Group.objects.create(
            name = 'delete_team',
        )

        delete_role = Role.objects.create(
            name = 'delete_team',
            organization = self.organization,
        )

        delete_role.permissions.set([delete_permissions])
        delete_role.groups.set([delete_group])

        self.delete_user.groups.set([delete_group])


        diff_org_group = Group.objects.create(
            name = 'diff_org_team',
        )

        diff_org_role = Role.objects.create(
            name = 'diff_org_team',
            organization = self.different_organization,
        )

        diff_org_role.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])
        diff_org_role.groups.set([diff_org_group])

        self.different_organization_user.groups.set([diff_org_group])



class PermissionsAPI(
    ViewSetBase,
    TestCase,
):


    def test_view_user_anon_has_permission(self):
        """ Check correct permission for view

        Attempt to view as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



@pytest.mark.module_devops
class ViewSet(
    ViewSetBase,
    SerializerView,
    TestCase
):


    def test_returned_serializer_user_view(self):
        """ Check correct Serializer is returned

        View action for view user must return `ViewSerializer`
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert str(response.renderer_context['view'].get_serializer().__class__.__name__).endswith('ViewSerializer')



    def test_view_cache_without_header_if_modified_since(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is not supplied the date is to
        be supplied to the client

        Status must be HTTP/200
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



    def test_view_cache_with_header_if_modified_since_changed(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client.

        Status must be HTTP/200
        """

        client = Client(
            headers = {
                'If-Modified-Since': datetime.fromtimestamp(
                    self.item.modified.timestamp() - 86400,
                    tz=tz.tzutc()
                    )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 200



    def test_view_cache_with_header_if_modified_since_no_changed_date_less(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client

        Status must be HTTP/304
        """

        client = Client(
            headers = {
                'If-Modified-Since': datetime.fromtimestamp(
                    self.item.modified.timestamp() + 3600,
                    tz=tz.tzutc()
                ).strftime(
                    '%a, %d %b %Y %H:%M:%S %z'
                )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 304



    def test_view_cache_with_header_if_modified_since_no_changed_date_same(self):
        """Data HTTP Caching Check

        if request header `If-Modified-Since` is supplied and the date is
        before the actual last modified date, supply the date to the client

        Status must be HTTP/304
        """

        client = Client(
            headers = {
                'If-Modified-Since': self.item.modified.strftime(
                    '%a, %d %b %Y %H:%M:%S %z'
                )
            }
        )

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 304



    def test_view_software_exists_feature_flagging_not_enabled_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        Even if the org exists, return not found so as to not leak that the org exists.
        Even if software exists, return not found so as to not leak if software exists

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['organization_id'] = self.different_organization.id

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404



    def test_view_software_not_exists_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        Just like when software exists, return not found so as not to allude to existance of software.

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['software_id'] = 99999

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404



    def test_view_organization_not_exists_rtn_404(self):
        """Data Leak check

        prevent leakage of other data not related to feature flagging

        just like if org exists, return not found so as not to allude to existance of organization.

        Status must be HTTP/404
        """

        client = Client()

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['organization_id'] = 99999

        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=url_view_kwargs)

        response = client.get(url)

        assert response.status_code == 404
