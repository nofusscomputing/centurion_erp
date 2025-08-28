import pytest

from django.apps import apps
from django.contrib.auth.models import ContentType, Permission

from access.models.tenant import Tenant
from centurion.tests.unit_class import ClassTestCases



@pytest.mark.model_centurionuser
class CenturionUserModelTestCases(
    ClassTestCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_group_permissions': {
                'type': bool,
                'value': False
            },
            '_tenancies': {
                'type': type(None),
                'value': None
            },
            '_tenancies_int': {
                'type': type(None),
                'value': None
            },
            '_permissions': {
                'type': type(None),
                'value': None
            },
            '_permissions_by_tenancy': {
                'type': type(None),
                'value': None
            },
            '_user_permissions': {
                'type': bool,
                'value': False
            },
        }



    @pytest.fixture( scope = 'function' )
    def centurion_user(self,
        django_db_blocker, model_instance,
        organization_one, organization_two, organization_three,
        model_role, kwargs_role,
        model_group, kwargs_group,
    ):

        with django_db_blocker.unblock():

            user = model_instance()

            yield user

            user.delete()



    @pytest.fixture( scope = 'function' )
    def group_roles(self,
        django_db_blocker,
        organization_one, model_permission,
        model_role, kwargs_role,
        model_group, kwargs_group,
    ):

        with django_db_blocker.unblock():

            kwargs = kwargs_group.copy()
            kwargs['name'] = 'grp_1'
            group_1 = model_group.objects.create( **kwargs )


            kwargs = kwargs_role.copy()
            kwargs['name'] = 'role_group_1'
            kwargs['organization'] = organization_one
            role_group_1 = model_role.objects.create( **kwargs )

            group_1.roles.set([ role_group_1 ])

            org_permission = model_permission.objects.get(
                codename = 'view_tenant',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'tenant',
                )
            )

            role_group_1.permissions.set([ org_permission ])

            yield group_1

            role_group_1.delete()
            group_1.delete()

    @pytest.fixture( scope = 'function' )
    def user_roles(self,
        django_db_blocker,
        organization_two, model_permission,
        model_role, kwargs_role,
        centurion_user,
    ):

        with django_db_blocker.unblock():

            kwargs = kwargs_role.copy()
            kwargs['name'] = 'user_role'
            kwargs['organization'] = organization_two
            user_role = model_role.objects.create( **kwargs )

            centurion_user.roles.set([ user_role ])

            role_permission = model_permission.objects.get(
                codename = 'view_role',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'role',
                )
            )

            user_role.permissions.set([ role_permission ])

            yield user_role

            user_role.delete()



    @pytest.fixture( scope = 'class')
    def test_class(cls, model):

        if model._meta.abstract:

            class MockModel(model):
                class Meta:
                    app_label = 'core'
                    verbose_name = 'mock instance'
                    managed = False

            instance = MockModel()

        else:

            instance = model()

        yield instance

        del instance

        if 'mockmodel' in apps.all_models['core']:

            del apps.all_models['core']['mockmodel']



    def test_function_get_group_permissions_returns_permissions_default_is_by_tenancy(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        assert len(centurion_user.get_group_permissions()) == 1


    def test_function_get_group_permissions_returns_permissions_by_tenancy_has_correct_key(self,
        centurion_user, group_roles, organization_one
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        assert str( 'tenancy_' + str( int(organization_one)) ) in centurion_user.get_group_permissions()


    def test_function_get_group_permissions_returns_permissions_by_tenancy_has_correct_permission(
        self, centurion_user, group_roles, organization_one
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        perms = centurion_user.get_group_permissions()

        # must exist for test to pass
        assert len(perms[str( 'tenancy_' + str( int(organization_one)) )]) == 1

        assert 'access.view_tenant' in perms[str( 'tenancy_' + str( int(organization_one)) )]


    def test_function_get_group_permissions_by_tenancy_cache_results(
        self, centurion_user, group_roles, organization_one, mocker
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        groups = mocker.spy(type(centurion_user.groups), "prefetch_related")

        centurion_user.get_group_permissions()    # Cache data

        groups.reset_mock()

        centurion_user.get_group_permissions()    # use cached data

        groups.assert_not_called()



    def test_function_get_group_permissions_returns_permissions_by_tenancy_adds_global_org(
        self, centurion_user, group_roles, organization_one, model_appsettings, organization_three
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        app_settings = model_appsettings.objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

        app_settings.global_organization = organization_three
        app_settings.save()

        centurion_user.get_group_permissions()

        # both orgs must exist for test to pass
        assert len(centurion_user._tenancies) == 2

        assert organization_three in centurion_user._tenancies





    def test_function_get_group_permissions_returns_permissions_list(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.groups.set([ group_roles ])

        assert len(centurion_user.get_group_permissions( tenancy = False )) == 1


    def test_function_get_group_permissions_returns_permissions_list_has_correct_permission(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.groups.set([ group_roles ])

        perms = centurion_user.get_group_permissions( tenancy = False )

        # must exist for test to pass
        assert len(perms) == 1

        assert 'access.view_tenant' in perms


    def test_function_get_group_permissions_list_cache_results(
        self, centurion_user, group_roles, organization_one, mocker
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        groups = mocker.spy(type(centurion_user.groups), "prefetch_related")

        centurion_user.get_group_permissions( tenancy = False )    # Cache data

        groups.reset_mock()

        centurion_user.get_group_permissions( tenancy = False )    # use cached data

        groups.assert_not_called()


    def test_function_get_group_permissions_returns_permissions_list_adds_global_org(
        self, centurion_user, group_roles, organization_one, model_appsettings, organization_three
    ):
        """Test function get_group_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])

        app_settings = model_appsettings.objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

        app_settings.global_organization = organization_three
        app_settings.save()

        centurion_user.get_group_permissions( tenancy = False )

        # both orgs must exist for test to pass
        assert len(centurion_user._tenancies) == 2

        assert organization_three in centurion_user._tenancies










    def test_function_get_permissions_returns_permissions_default_is_by_tenancy(self,
        centurion_user, group_roles, user_roles,
    ):
        """Test function get_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        assert len(centurion_user.get_permissions()) == 2


    def test_function_get_permissions_returns_permissions_by_tenancy_has_correct_key(self,
        centurion_user, group_roles, organization_one, organization_two, user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        assert str( 'tenancy_' + str( int(organization_one)) ) in centurion_user.get_permissions()
        assert str( 'tenancy_' + str( int(organization_two)) ) in centurion_user.get_permissions()


    def test_function_get_permissions_returns_permissions_by_tenancy_has_correct_permission(
        self, centurion_user, group_roles, organization_one, organization_two, user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        perms = centurion_user.get_permissions()

        # must exist for test to pass
        assert len(perms[str( 'tenancy_' + str( int(organization_one)) )]) == 1
        assert len(perms[str( 'tenancy_' + str( int(organization_two)) )]) == 1

        assert 'access.view_tenant' in perms[str( 'tenancy_' + str( int(organization_one)) )]
        assert 'access.view_role' in perms[str( 'tenancy_' + str( int(organization_two)) )]


    def test_function_get_permissions_by_tenancy_cache_results(
        self, centurion_user, group_roles, organization_one, mocker, user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        groups = mocker.spy(type(centurion_user.groups), "prefetch_related")
        roles = mocker.spy(type(centurion_user.roles), "prefetch_related")

        centurion_user.get_permissions()    # Cache data

        groups.reset_mock()
        roles.reset_mock()

        centurion_user.get_permissions()    # use cached data

        groups.assert_not_called()
        roles.assert_not_called()



    def test_function_get_permissions_returns_permissions_by_tenancy_adds_global_org(
        self, centurion_user, group_roles, model_appsettings,
        organization_three, user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        app_settings = model_appsettings.objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

        app_settings.global_organization = organization_three
        app_settings.save()

        centurion_user.get_permissions()

        # both orgs must exist for test to pass
        assert len(centurion_user._tenancies) == 3

        assert organization_three in centurion_user._tenancies




    def test_function_get_permissions_returns_permissions_list(self,
        centurion_user, group_roles, user_roles,
    ):
        """Test function get_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        assert len(centurion_user.get_permissions( tenancy = False )) == 2


    def test_function_get_permissions_returns_permissions_list_has_correct_permission(self,
        centurion_user, group_roles, user_roles,
    ):
        """Test function get_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        perms = centurion_user.get_permissions( tenancy = False )

        # must exist for test to pass
        assert len(perms) == 2

        assert 'access.view_tenant' in perms


    def test_function_get_permissions_list_cache_results(
        self, centurion_user, group_roles, mocker, user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        groups = mocker.spy(type(centurion_user.groups), "prefetch_related")
        roles = mocker.spy(type(centurion_user.roles), "prefetch_related")

        centurion_user.get_permissions( tenancy = False )    # Cache data

        groups.reset_mock()
        roles.reset_mock()

        centurion_user.get_permissions( tenancy = False )    # use cached data

        groups.assert_not_called()
        roles.assert_not_called()


    def test_function_get_permissions_returns_permissions_list_adds_global_org(
        self, centurion_user, group_roles, model_appsettings, organization_three,
        user_roles,
    ):
        """Test function get_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.groups.set([ group_roles ])
        centurion_user.roles.set([ user_roles ])


        app_settings = model_appsettings.objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

        app_settings.global_organization = organization_three
        app_settings.save()

        centurion_user.get_permissions( tenancy = False )

        # both orgs must exist for test to pass
        assert len(centurion_user._tenancies) == 3

        assert organization_three in centurion_user._tenancies









    def test_function_get_tenancies_default_no_args(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        assert len(centurion_user.get_tenancies()) == 1


    def test_function_get_tenancies_calls_get_group_permissions(self,
        centurion_user, mocker, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        groups = mocker.spy(centurion_user, "get_group_permissions")

        groups.reset_mock()
        centurion_user.get_tenancies()

        groups.assert_called_once()


    def test_function_get_tenancies_calls_get_user_permissions(self,
        centurion_user, mocker, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        user = mocker.spy(centurion_user, "get_user_permissions")

        user.reset_mock()
        centurion_user.get_tenancies()

        user.assert_called_once()


    def test_function_get_tenancies_default_int_list_true(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        tenancies = centurion_user.get_tenancies( int_list = True )

        assert len(tenancies) == 1    # must exist and only be one

        assert isinstance(tenancies[0], int)


    def test_function_get_tenancies_default_int_list_false(self,
        centurion_user, group_roles
    ):
        """Test function get_group_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        tenancies = centurion_user.get_tenancies( int_list = False )

        assert len(tenancies) == 1    # must exist and only be one

        assert isinstance(tenancies[0], Tenant)

















    def test_function_get_user_permissions_returns_permissions_default_is_by_tenancy(self,
        centurion_user, user_roles
    ):
        """Test function get_user_permissions

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.roles.set([ user_roles ])

        assert len(centurion_user.get_user_permissions()) == 1


    def test_function_get_user_permissions_returns_permissions_by_tenancy_has_correct_key(self,
        centurion_user, user_roles, organization_two
    ):
        """Test function get_user_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.roles.set([ user_roles ])

        assert str( 'tenancy_' + str( int(organization_two)) ) in centurion_user.get_user_permissions()


    def test_function_get_user_permissions_returns_permissions_by_tenancy_has_correct_permission(
        self, centurion_user, user_roles, organization_two
    ):
        """Test function get_user_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.roles.set([ user_roles ])

        perms = centurion_user.get_user_permissions()

        # must exist for test to pass
        assert len(perms[str( 'tenancy_' + str( int(organization_two)) )]) == 1

        assert 'access.view_role' in perms[str( 'tenancy_' + str( int(organization_two)) )]


    def test_function_get_user_permissions_by_tenancy_cache_results(
        self, centurion_user, user_roles, organization_one, mocker
    ):
        """Test function get_user_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.roles.set([ user_roles ])

        groups = mocker.spy(type(centurion_user.roles), "prefetch_related")

        centurion_user.get_user_permissions()    # Cache data

        groups.reset_mock()

        centurion_user.get_user_permissions()    # use cached data

        groups.assert_not_called()





    def test_function_get_user_permissions_returns_permissions_list(self,
        centurion_user, user_roles
    ):
        """Test function get_user_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.roles.set([ user_roles ])

        assert len(centurion_user.get_user_permissions( tenancy = False )) == 1


    def test_function_get_user_permissions_returns_permissions_list_has_correct_permission(self,
        centurion_user, user_roles
    ):
        """Test function get_user_permissions

        when calling with arg `tenancy = False` return permmissions in list
        """

        centurion_user.roles.set([ user_roles ])

        perms = centurion_user.get_user_permissions( tenancy = False )

        # must exist for test to pass
        assert len(perms) == 1

        assert 'access.view_role' in perms


    def test_function_get_user_permissions_list_cache_results(
        self, centurion_user, user_roles, mocker
    ):
        """Test function get_user_permissions

        Ensure the dict key name is `tenancy_<tenancy_id>`
        """

        centurion_user.roles.set([ user_roles ])

        groups = mocker.spy(type(centurion_user.roles), "prefetch_related")

        centurion_user.get_user_permissions( tenancy = False )    # Cache data

        groups.reset_mock()

        centurion_user.get_user_permissions( tenancy = False )    # use cached data

        groups.assert_not_called()












    def test_function_has_perm_group_no_obj_no_tenancy(self,
        centurion_user, group_roles
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        with pytest.raises(ValueError):

            centurion_user.has_perm(
                permission = 'access.view_tenant',
                obj = None,
                tenancy = None
            )


    def test_function_has_perm_group_with_obj_no_tenancy(self,
        centurion_user, group_roles, organization_one
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        class MockTenancyObject:
            def get_tenant(self):
                return organization_one


        centurion_user.groups.set([ group_roles ])

        assert centurion_user.has_perm(
            permission = 'access.view_tenant',
            obj = MockTenancyObject(),
            tenancy = None
        )

    def test_function_has_perm_group_no_obj_with_tenancy(self,
        centurion_user, group_roles, organization_one
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        assert centurion_user.has_perm(
            permission = 'access.view_tenant',
            obj = None,
            tenancy = organization_one
        )



    def test_function_has_perm_group_with_obj_no_tenancy_wrong_tenancy(self,
        centurion_user, group_roles, organization_two
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        class MockTenancyObject:
            def get_tenant(self):
                return organization_two


        centurion_user.groups.set([ group_roles ])

        assert not centurion_user.has_perm(
            permission = 'access.view_tenant',
            obj = MockTenancyObject(),
            tenancy = None
        )

    def test_function_has_perm_group_no_obj_with_tenancy_wrong_tenancy(self,
        centurion_user, group_roles, organization_two
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.groups.set([ group_roles ])

        assert not centurion_user.has_perm(
            permission = 'access.view_tenant',
            obj = None,
            tenancy = organization_two
        )







    def test_function_has_perm_user_no_obj_no_tenancy(self,
        centurion_user, user_roles
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.roles.set([ user_roles ])

        with pytest.raises(ValueError):

            centurion_user.has_perm(
                permission = 'access.view_role',
                obj = None,
                tenancy = None
            )


    def test_function_has_perm_user_with_obj_no_tenancy(self,
        centurion_user, user_roles, organization_two
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        class MockTenancyObject:
            def get_tenant(self):
                return organization_two


        centurion_user.roles.set([ user_roles ])

        assert centurion_user.has_perm(
            permission = 'access.view_role',
            obj = MockTenancyObject(),
            tenancy = None
        )

    def test_function_has_perm_user_no_obj_with_tenancy(self,
        centurion_user, user_roles, organization_two
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.roles.set([ user_roles ])

        assert centurion_user.has_perm(
            permission = 'access.view_role',
            obj = None,
            tenancy = organization_two
        )





    def test_function_has_perm_user_with_obj_no_tenancy_wrong_tenancy(self,
        centurion_user, user_roles, organization_one
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        class MockTenancyObject:
            def get_tenant(self):
                return organization_one


        centurion_user.roles.set([ user_roles ])

        assert not centurion_user.has_perm(
            permission = 'access.view_role',
            obj = MockTenancyObject(),
            tenancy = None
        )

    def test_function_has_perm_user_no_obj_with_tenancy_wrong_tenancy(self,
        centurion_user, user_roles, organization_one
    ):
        """Test function has_perm

        when calling with no args, return the permissions by tenancy
        """

        centurion_user.roles.set([ user_roles ])

        assert not centurion_user.has_perm(
            permission = 'access.view_role',
            obj = None,
            tenancy = organization_one
        )










class CenturionUserModelInheritedCases(
    CenturionUserModelTestCases,
):
    pass



@pytest.mark.module_access
class CenturionUserModelPyTest(
    CenturionUserModelTestCases,
):
    pass
