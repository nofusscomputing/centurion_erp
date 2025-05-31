import django
import pytest

from settings.models.app_settings import AppSettings


User = django.contrib.auth.get_user_model()



@pytest.fixture( scope = 'class')
def api_request_permissions( django_db_blocker,
    model_contenttype,
    model_permission,
    model,
    organization_one,
    organization_two,
    organization_three,
):

    with django_db_blocker.unblock():


        random_str = datetime.datetime.now(tz=datetime.timezone.utc)

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

        add_team = Team.objects.create(
            team_name = 'add_team' + str(random_str),
            organization = organization_one,
        )

        add_team.permissions.set([add_permissions])

        add_user = User.objects.create_user(
            username="test_user_add" + str(random_str), password="password"
        )

        TeamUsers.objects.create(
            team = add_team,
            user = add_user
        )



        change_permissions = model_permission.objects.get(
                codename = 'change_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team' + str(random_str),
            organization = organization_one,
        )

        change_team.permissions.set([change_permissions])

        change_user = User.objects.create_user(
            username="test_user_change" + str(random_str), password="password"
        )

        TeamUsers.objects.create(
            team = change_team,
            user = change_user
        )



        delete_permissions = model_permission.objects.get(
                codename = 'delete_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team' + str(random_str),
            organization = organization_one,
        )

        delete_team.permissions.set([delete_permissions])

        delete_user = User.objects.create_user(
            username="test_user_delete" + str(random_str), password="password"
        )
        TeamUsers.objects.create(
            team = delete_team,
            user = delete_user
        )



        view_permissions = model_permission.objects.get(
                codename = 'view_' + model._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team' + str(random_str),
            organization = organization_one,
        )

        view_team.permissions.set([view_permissions])

        view_user = User.objects.create_user(
            username="test_user_view" + str(random_str), password="password"
        )

        TeamUsers.objects.create(
            team = view_team,
            user = view_user
        )



        different_organization_user = User.objects.create_user(
            username="test_diff_org_user" + str(random_str), password="password"
        )


        different_organization_team = Team.objects.create(
            team_name = 'diff_org_team' + str(random_str),
            organization = organization_two,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = different_organization_user
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
                'change': change_user,
                'delete': delete_user,
                'different_tenancy': different_organization_user,
                'no_permissions': '',
                'view': view_user,
            }

        }

        add_team.delete()
        add_user.delete()

        change_team.delete()
        change_user.delete()

        delete_team.delete()
        delete_user.delete()

        view_team.delete()
        view_user.delete()

        different_organization_team.delete()
        different_organization_user.delete()
