import pytest
import random

from settings.models.app_settings import AppSettings



@pytest.fixture( scope = 'class')
def api_request_permissions( django_db_blocker,
    model_contenttype,
    model_group,
    model_permission,
    model_role,
    model_user,
    model,
    organization_one,
    organization_two,
    organization_three,
):

    with django_db_blocker.unblock():

        random_str = str(random.randint(1, 99999))

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = organization_three

        app_settings.save()


        add_permissions = model_permission.objects.get(
                codename = 'add_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        add_user = model_user.objects.create_user(
            username="test_user_add" + str(random_str), password="password"
        )


        add_group = model_group.objects.create(
            name = 'add_team' + str(random_str),
        )

        add_user.groups.set( [ add_group ])

        add_role = model_role.objects.create(
            organization = organization_one,
            name = 'add_role' + str(random_str),
        )

        add_role.groups.set( [ add_group ] )
        add_role.permissions.set( [ add_permissions ] )


        change_permissions = model_permission.objects.get(
                codename = 'change_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        change_user = model_user.objects.create_user(
            username="test_user_change" + str(random_str), password="password"
        )

        change_group = model_group.objects.create(
            name = 'change_team' + str(random_str),
        )

        change_user.groups.set( [ change_group ])

        change_role = model_role.objects.create(
            organization = organization_one,
            name = 'change_role' + str(random_str),
        )

        change_role.groups.set( [ change_group ] )
        change_role.permissions.set( [ change_permissions ] )



        delete_permissions = model_permission.objects.get(
                codename = 'delete_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        delete_user = model_user.objects.create_user(
            username="test_user_delete" + str(random_str), password="password"
        )

        delete_group = model_group.objects.create(
            name = 'delete_team' + str(random_str),
        )

        delete_user.groups.set( [ delete_group ])

        delete_role = model_role.objects.create(
            organization = organization_one,
            name = 'delete_role' + str(random_str),
        )

        delete_role.groups.set( [ delete_group ] )
        delete_role.permissions.set( [ delete_permissions ] )



        view_permissions = model_permission.objects.get(
                codename = 'view_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        view_user = model_user.objects.create_user(
            username="api_r_perm_user_view" + str(random_str), password="password"
        )

        view_group = model_group.objects.create(
            name = 'view_team' + str(random_str),
        )

        view_user.groups.set( [ view_group ])

        view_role = model_role.objects.create(
            organization = organization_one,
            name = 'view_role' + str(random_str),
        )

        view_role.groups.set( [ view_group ] )
        view_role.permissions.set( [ view_permissions ] )



        different_organization_user = model_user.objects.create_user(
            username="test_diff_org_user" + str(random_str), password="password"
        )


        different_organization_group = model_group.objects.create(
            name = 'diff_org_team' + str(random_str),
        )

        different_organization_user.groups.set( [ different_organization_group ])

        different_organization_role = model_role.objects.create(
            organization = organization_two,
            name = 'diff_org_team' + str(random_str),
        )

        different_organization_role.groups.set( [ different_organization_group ] )
        different_organization_role.permissions.set( [
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])





        no_permission_user = model_user.objects.create_user(
            username="nil_permissions" + str(random_str), password="password"
        )


        yield {
            'app_settings': app_settings,
            'tenancy': {
                'different': organization_two,
                'global': organization_three,
                'user': organization_one
            },
            'user': {
                'add': add_user,
                'anon': None,
                'change': change_user,
                'delete': delete_user,
                'different_tenancy': different_organization_user,
                'no_permissions': no_permission_user,
                'view': view_user,
            }

        }

        #
        # Commented out as meta class tests fail due to fixture being cleaned before test is 
        # completed.
        #
        # add_team.delete()
        # add_user.delete()

        # change_team.delete()
        # change_user.delete()

        # delete_team.delete()
        # delete_user.delete()

        # view_team.delete()
        # view_user.delete()

        # different_organization_team.delete()
        # different_organization_user.delete()
