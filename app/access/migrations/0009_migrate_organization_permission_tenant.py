
from django.contrib.auth.models import ContentType, Permission
from django.db import migrations

from access.models.team import Team

ContentType.DoesNotExist

def add_tenancy_permissions(apps, schema_editor):

    print('')
    print(f"Begin permission migration for rename of Organization to Tenant.")

    try:

        add_permission = Permission.objects.get(
                codename = 'add_tenant',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'tenant',
                )
            )

        change_permission = Permission.objects.get(
                codename = 'change_tenant',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'tenant',
                )
            )

        delete_permission = Permission.objects.get(
                codename = 'delete_tenant',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'tenant',
                )
            )

        view_permission = Permission.objects.get(
                codename = 'view_tenant',
                content_type = ContentType.objects.get(
                    app_label = 'access',
                    model = 'tenant',
                )
            )

        print(f'    Searching for Teams.')

        teams = Team.objects.select_related('group_ptr__permissions')

        print(f'Found {str(len(teams))} Teams.')

        for team in teams:

            print(f'    Processing Team {str(team.team_name)}.')

            permissions = team.group_ptr.permissions.all()

            print(f'    Searching for Organization Permissions.')
            print(f'    Found {str(len(permissions))} Permissions.')

            for permission in permissions:

                if '_organization' not in permission.codename:

                    continue

                action = str(permission.codename).split('_')[0]

                print(f'        Found Organization Permission {str(action)}')

                if action == 'add':

                    team.group_ptr.permissions.add( add_permission )

                    print(f'        Add Tenant Permission {str(action)}')

                    team.group_ptr.permissions.remove( permission )

                    print(f'        Remove Organization Permission {str(action)}')

                elif action == 'change':

                    team.group_ptr.permissions.add( change_permission )

                    print(f'        Add Tenant Permission {str(action)}')

                    team.group_ptr.permissions.remove( permission )

                    print(f'        Remove Organization Permission {str(action)}')

                elif action == 'delete':

                    team.group_ptr.permissions.add( delete_permission )

                    print(f'        Add Tenant Permission {str(action)}')

                    team.group_ptr.permissions.remove( permission )

                    print(f'        Remove Organization Permission {str(action)}')

                elif action == 'view':

                    team.group_ptr.permissions.add( view_permission )

                    print(f'        Add Tenant Permission {str(action)}')

                    team.group_ptr.permissions.remove( permission )

                    print(f'        Remove Organization Permission {str(action)}')


            print(f'    Completed Team {str(team.team_name)}.')

    except ContentType.DoesNotExist:
        # DB is new so no content types. no migration to be done.
        pass

    print('  Permission Migration Actions Complete.')




class Migration(migrations.Migration):

    dependencies = [
        ('access', '0008_alter_tenant_options_alter_entity_organization_and_more'),
    ]

    operations = [
        migrations.RunPython(add_tenancy_permissions),
    ]


