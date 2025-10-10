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

        app_settings = AppSettings.objects.filter(
            owner_organization = None
        )[0]

        app_settings.global_organization = organization_three

        app_settings.save()

        if not model._meta.abstract:

            add_permissions = model_permission.objects.get(
                    codename = 'add_' + model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = model._meta.app_label,
                        model = model._meta.model_name,
                    )
                )

            add_user = model_user.objects.create_user(
                username="api_rp_user_add" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
            )


            add_group = model_group.objects.create(
                name = 'add_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            add_user.groups.set( [ add_group ])

            add_role = model_role.objects.create(
                organization = organization_one,
                name = 'add_role' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            add_role.groups.set( [ add_group ] )
            add_role.permissions.set( [ add_permissions ] )

            # add user to different org, however no perms
            role_diff_org = model_role.objects.create(
                organization = organization_two,
                name = 'role_diff_org' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            role_diff_org.groups.set( [ add_group ] )

            change_permissions = model_permission.objects.get(
                    codename = 'change_' + model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = model._meta.app_label,
                        model = model._meta.model_name,
                    )
                )

            change_user = model_user.objects.create_user(
                username="api_rp_user_change" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
            )

            change_group = model_group.objects.create(
                name = 'change_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            change_user.groups.set( [ change_group ])

            change_role = model_role.objects.create(
                organization = organization_one,
                name = 'change_role' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            role_diff_org.groups.set( [ change_group ] )
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
                username="api_rp_user_delete" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
            )

            delete_group = model_group.objects.create(
                name = 'delete_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            delete_user.groups.set( [ delete_group ])

            delete_role = model_role.objects.create(
                organization = organization_one,
                name = 'delete_role' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            role_diff_org.groups.set( [ delete_group ] )
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
                username="api_r_perm_user_view" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
            )

            view_group = model_group.objects.create(
                name = 'view_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            view_user.groups.set( [ view_group ])

            view_role = model_role.objects.create(
                organization = organization_one,
                name = 'view_role' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            role_diff_org.groups.set( [ view_group ] )
            view_role.groups.set( [ view_group ] )
            view_role.permissions.set( [ view_permissions ] )



            different_organization_user = model_user.objects.create_user(
                username="api_rp_diff_org_user" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
            )


            different_organization_group = model_group.objects.create(
                name = 'diff_org_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            different_organization_user.groups.set( [ different_organization_group ])

            different_organization_role = model_role.objects.create(
                organization = organization_two,
                name = 'diff_org_team' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            )

            different_organization_role.groups.set( [ different_organization_group ] )
            different_organization_role.permissions.set( [
                view_permissions,
                add_permissions,
                change_permissions,
                delete_permissions,
            ])





            no_permission_user = model_user.objects.create_user(
                username="api_rp_nil_permissions" + str( random.randint(1,999) ) + str( random.randint(1,999) ), password="password"
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
            add_role.delete()
            add_group.delete()
            add_user.delete()

            change_role.delete()
            change_group.delete()
            change_user.delete()

            delete_role.delete()
            delete_group.delete()
            delete_user.delete()

            view_role.delete()
            view_group.delete()
            view_user.delete()

            different_organization_role.delete()
            different_organization_group.delete()
            different_organization_user.delete()

            no_permission_user.delete()


        else:
            yield {
                'app_settings': app_settings,
                'tenancy': {
                    'different': organization_two,
                    'global': organization_three,
                    'user': organization_one
                },
                # 'user': {
                #     'add': add_user,
                #     'anon': None,
                #     'change': change_user,
                #     'delete': delete_user,
                #     'different_tenancy': different_organization_user,
                #     'no_permissions': no_permission_user,
                #     'view': view_user,
                # }

            }