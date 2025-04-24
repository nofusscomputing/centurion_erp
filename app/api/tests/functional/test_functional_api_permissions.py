import pytest

from django.contrib.auth.models import ContentType, Permission, User
from django.shortcuts import reverse
from django.test import Client

from access.models.team import Team
from access.models.team_user import TeamUsers



class APIPermissionAddInheritedCases:
    """ Test Suite for Add API Permission test cases """


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_list: str
    """ URL view name of the item list page """

    url_kwargs: dict = None
    """ URL view kwargs for the item list page """

    add_data: dict = None

    permission_no_add = [
            ('anon_user_auth_required', None, 401),
            ('change_user_forbidden', 'change_user', 403),
            ('delete_user_forbidden', 'delete_user', 403),
            ('different_organization_user_forbidden', 'different_organization_user', 403),
            ('no_permission_user_forbidden', 'no_permissions_user', 403),
            ('view_user_forbidden', 'view_user', 403),
        ]

    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_add, 
        ids=[test_name for test_name, user, expected in permission_no_add]
    )
    def test_permission_no_add(self, test_name, user, expected):
        """ Check correct permission for add

        Attempt to add as user with no permissions
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        if user is not None:

            client.force_login( getattr(self, user) )

        response = client.post(url, data=self.add_data)

        assert response.status_code == int(expected)



    def test_permission_add(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 201



class APIPermissionChangeInheritedCases:
    """ Test Suite for Change API Permission test cases """

    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    change_data: dict = None

    permission_no_change = [
            ('add_user_forbidden', 'add_user', 403),
            ('anon_user_auth_required', None, 401),
            ('delete_user_forbidden', 'delete_user', 403),
            ('different_organization_user_forbidden', 'different_organization_user', 403),
            ('no_permission_user_forbidden', 'no_permissions_user', 403),
            ('view_user_forbidden', 'view_user', 403),
        ]



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_change, 
        ids=[test_name for test_name, user, expected in permission_no_change]
    )
    def test_permission_no_change(self, test_name, user, expected):
        """ Ensure permission view cant make change

        Attempt to make change as user without permissions
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        if user is not None:

            client.force_login( getattr(self, user) )

        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == int(expected)


    def test_permission_change(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 200



class APIPermissionDeleteInheritedCases:
    """ Test Suite for Delete API Permission test cases """


    model: object
    """ Item Model to test """

    app_namespace: str = None
    """ URL namespace """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """

    delete_data: dict = None

    permission_no_delete = [
            ('add_user_forbidden', 'add_user', 403),
            ('anon_user_auth_required', None, 401),
            ('change_user_forbidden', 'change_user', 403),
            ('different_organization_user_forbidden', 'different_organization_user', 403),
            ('no_permission_user_forbidden', 'no_permissions_user', 403),
            ('view_user_forbidden', 'view_user', 403),
        ]



    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_delete, 
        ids=[test_name for test_name, user, expected in permission_no_delete]
    )
    def test_permission_no_delete(self, test_name, user, expected):
        """ Check correct permission for delete

        Attempt to delete as user with no permissons
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        if user is not None:

            client.force_login( getattr(self, user) )

        response = client.delete(url, data=self.delete_data)

        assert response.status_code == int(expected)


    def test_permission_delete(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 204



class APIPermissionViewInheritedCases:
    """ Test Suite for View API Permission test cases """

    app_namespace: str = None
    """ URL namespace """

    model: object
    """ Item Model to test """

    url_name: str
    """ URL name of the view to test """

    url_view_kwargs: dict = None
    """ URL kwargs of the item page """


    permission_no_view = [
        ('add_user_forbidden', 'add_user', 403),
        ('anon_user_auth_required', None, 401),
        ('change_user_forbidden', 'change_user', 403),
        ('delete_user_forbidden', 'delete_user', 403),
        ('different_organization_user_forbidden', 'different_organization_user', 403),
        ('no_permission_user_forbidden', 'no_permissions_user', 403),
    ]

    @pytest.mark.parametrize(
        argnames = "test_name, user, expected",
        argvalues = permission_no_view, 
        ids=[test_name for test_name, user, expected in permission_no_view]
    )
    def test_permission_no_view(self, test_name, user, expected):
        """ Check correct permission for view

        Attempt to view with user missing permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        if user is not None:

            client.force_login(getattr(self, user))

        response = client.get(url)

        assert response.status_code == int(expected)



    def test_permission_view(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200



    def test_returned_results_only_user_orgs(self):
        """Returned results check

        Ensure that a query to the viewset endpoint does not return
        items that are not part of the users organizations.
        """

        # Ensure the other org item exists, without test not able to function
        print('Check that the different organization item has been defined')
        assert hasattr(self, 'other_org_item')

        # ensure that the variables for the two orgs are different orgs
        print('checking that the different and user oganizations are different')
        assert self.different_organization.id != self.organization.id


        client = Client()

        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        viewable_organizations = [
            self.organization.id,
        ]

        if getattr(self, 'global_organization', None):    # Cater for above test that also has global org

            viewable_organizations += [ self.global_organization.id ]



        client.force_login(self.view_user)
        response = client.get(url)

        contains_different_org: bool = False

        for item in response.data['results']:

            if int(item['organization']['id']) not in viewable_organizations:

                contains_different_org = True
                print(f'Failed returned row was: {item}')

        assert not contains_different_org



    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_kwargs)


        only_from_user_org: bool = True

        viewable_organizations = [
            self.organization.id,
            self.global_organization.id
        ]


        assert getattr(self.global_organization, 'id', False)    # fail if no global org set
        assert getattr(self.global_org_item, 'id', False)    # fail if no global item set


        client.force_login(self.view_user)
        response = client.get(url)

        assert len(response.data['results']) >= 2    # fail if only one item extist.


        for row in response.data['results']:

            if row['organization']['id'] not in viewable_organizations:

                only_from_user_org = False

                print(f'Users org: {self.organization.id}')
                print(f'global org: {self.global_organization.id}')
                print(f'Failed returned row was: {row}')

        assert only_from_user_org



class APIPermissionsInheritedCases(
    APIPermissionAddInheritedCases,
    APIPermissionChangeInheritedCases,
    APIPermissionDeleteInheritedCases,
    APIPermissionViewInheritedCases
):
    """ Test Suite for all API Permission test cases """

    model: object
    """ Item Model to test """

    permission_no_add: list = []

    permission_no_change: list = []

    permission_no_delete: list = []

    permission_no_view: list = []


    @classmethod
    def setup_class(self):


        self.permission_no_add = [
            *super().permission_no_add,
            *self.permission_no_add,
        ]

        self.permission_no_change = [
            *super().permission_no_change,
            *self.permission_no_change,
        ]

        self.permission_no_delete = [
            *super().permission_no_delete,
            *self.permission_no_delete,
        ]

        self.permission_no_view = [
            *super().permission_no_view,
            *self.permission_no_view,
        ]


    @pytest.fixture(scope='class')
    def var_setup(self, request):


            kwargs_create_item = {}

            kwargs_create_item_diff_org = {}

            url_kwargs = {}

            url_view_kwargs = {}

            for base in reversed(request.cls.__mro__):

                if hasattr(base, 'kwargs_create_item'):

                    if base.kwargs_create_item is not None:

                        kwargs_create_item.update(**base.kwargs_create_item)

                if hasattr(base, 'kwargs_create_item_diff_org'):

                    if base.kwargs_create_item_diff_org is not None:

                        kwargs_create_item_diff_org.update(**base.kwargs_create_item_diff_org)

                if hasattr(base, 'url_kwargs'):

                    if base.url_kwargs is not None:

                        url_kwargs.update(**base.url_kwargs)

                if hasattr(base, 'url_view_kwargs'):

                    if base.url_view_kwargs is not None:

                        url_view_kwargs.update(**base.url_view_kwargs)


            request.cls.kwargs_create_item = kwargs_create_item
            request.cls.kwargs_create_item_diff_org = kwargs_create_item_diff_org
            request.cls.url_kwargs = url_kwargs
            request.cls.url_view_kwargs = url_view_kwargs

            yield

            del request.cls.kwargs_create_item

            del request.cls.kwargs_create_item_diff_org

            del request.cls.url_kwargs

            del request.cls.url_view_kwargs



    @pytest.fixture(scope='class')
    def prepare(self, request, django_db_blocker,
        organization_one,
        organization_two,
    ):

        with django_db_blocker.unblock():

            if not hasattr(request.cls, 'organization'):

                request.cls.organization = organization_one

            
            if not hasattr(request.cls, 'different_organization'):

                request.cls.different_organization = organization_two


            request.cls.view_user = User.objects.create_user(username="func_api_perms_test_user_view", password="password")


            request.cls.kwargs_create_item.update({
                'organization': request.cls.organization,
                'opened_by': request.cls.view_user
            })

            request.cls.kwargs_create_item_diff_org.update({
                'organization': request.cls.different_organization,
                'opened_by': request.cls.view_user
            })

            request.cls.other_org_item = request.cls.model.objects.create(
                **request.cls.kwargs_create_item_diff_org
            )


            if request.cls.add_data is not None:

                request.cls.add_data.update({
                    'organization': request.cls.organization.id,
                    'opened_by': request.cls.view_user.pk
                })

            view_permissions = Permission.objects.get(
                    codename = 'view_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )


            add_permissions = Permission.objects.get(
                    codename = 'add_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )


            change_permissions = Permission.objects.get(
                    codename = 'change_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )


            delete_permissions = Permission.objects.get(
                    codename = 'delete_' + request.cls.model._meta.model_name,
                    content_type = ContentType.objects.get(
                        app_label = request.cls.model._meta.app_label,
                        model = request.cls.model._meta.model_name,
                    )
                )


            add_team = Team.objects.create(
                team_name = 'func_api_perms_add_team',
                organization = request.cls.organization,
            )

            add_team.permissions.set([add_permissions])


            change_team = Team.objects.create(
                team_name = 'func_api_perms_change_team',
                organization = request.cls.organization,
            )

            change_team.permissions.set([change_permissions])


            delete_team = Team.objects.create(
                team_name = 'func_api_perms_delete_team',
                organization = request.cls.organization,
            )

            delete_team.permissions.set([delete_permissions])


            view_team = Team.objects.create(
                team_name = 'func_api_perms_view_team',
                organization = request.cls.organization,
            )

            view_team.permissions.set([view_permissions])


            request.cls.no_permissions_user = User.objects.create_user(username="func_api_perms_no_permissions", password="password")

            request.cls.different_organization_user = User.objects.create_user(username="fc_api_perm_s__diff_org_user", password="password")

            different_organization_team = Team.objects.create(
                team_name = 'func_api_perms_diff_org_team',
                organization = request.cls.different_organization,
            )

            different_organization_team.permissions.set([
                view_permissions,
                add_permissions,
                change_permissions,
                delete_permissions,
            ])

            TeamUsers.objects.create(
                team = different_organization_team,
                user = request.cls.different_organization_user
            )


            request.cls.add_user = User.objects.create_user(username="func_api_perms__user_add", password="password")
            TeamUsers.objects.create(
                team = add_team,
                user = request.cls.add_user
            )

            request.cls.change_user = User.objects.create_user(username="func_api_perms__user_change", password="password")
            TeamUsers.objects.create(
                team = change_team,
                user = request.cls.change_user
            )

            request.cls.delete_user = User.objects.create_user(username="func_api_perms__user_delete", password="password")
            TeamUsers.objects.create(
                team = delete_team,
                user = request.cls.delete_user
            )

            TeamUsers.objects.create(
                team = view_team,
                user = request.cls.view_user
            )

            yield

            request.cls.other_org_item.delete()

            del request.cls.other_org_item


            request.cls.add_user.delete()

            add_team.delete()

            request.cls.change_user.delete()

            change_team.delete()

            request.cls.delete_user.delete()

            delete_team.delete()

            request.cls.view_user.delete()

            view_team.delete()

            request.cls.no_permissions_user.delete()

            request.cls.different_organization_user.delete()

            different_organization_team.delete()


    @pytest.fixture(scope='class', autouse = True)
    def post_model(self, request):

        request.cls.url_view_kwargs.update({ 'pk': request.cls.item.id })


    @pytest.fixture(scope='class', autouse = True)
    def class_setup(self, request, django_db_blocker,
        model,
        var_setup,
        prepare,
        create_model,
        post_model
    ):

        pass
