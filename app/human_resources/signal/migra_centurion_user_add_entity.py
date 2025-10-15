from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models.signals import (
    post_migrate,
)
from django.dispatch import receiver

# from core.mixins.centurion import Centurion


@receiver(post_migrate, dispatch_uid="centurion_user_add_entity")
def centurion_user_add_entity(sender, **kwargs):


    if sender.label != 'human_resources':
        return

    

    try:

        all_users = apps.get_model(settings.AUTH_USER_MODEL).objects.all()
        system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
            username = 'system'
        ).first()

        if all_users:
            print('\n\nFetching Users.\n')


        for user in all_users:

            try:

                if(
                    user.get_entity()
                    or user.username == 'system'
                    or user.first_name in [None, '']
                    or user.last_name in [None, '']
                ):
                    continue

                # organization = apps.get_model(
                #     app_label = 'core',
                #     model_name = 'centurionaudit'
                # ).objects.filter(
                #     user = user
                # ).annotate(org_count=Count('organization')).order_by('-org_count')

                organization = apps.get_model(
                    app_label = 'core',
                    model_name = 'centurionaudit'
                ).objects.filter(
                    user=user
                ).values(
                    'organization'
                ).annotate(
                    org_count=Count('organization')
                ).order_by(
                    '-org_count'
                ).first()

                print( f'    Processing user {user.username}.....' )

                random_int = int( str(datetime.now().strftime("%y%m%d%H%M%S")) + f"{datetime.now().microsecond // 100:04d}" )

                email = user.email

                if email in [None, '']:
                    email = f'no_email.{random_int}@noreply.local'


                entity_kwargs = {
                    'organization': apps.get_model(
                        app_label = 'access',
                        model_name = 'tenant'
                    ).objects.get(
                        id = organization['organization']
                    ),
                    'employee_number':  random_int,
                    'f_name': user.first_name,
                    'l_name': user.last_name,
                    'email': email,
                    'directory': False,
                    'user': user,
                    'model_notes': 'Employee Auto-added during migration.\n\n**please audit** to ensure that the employee details are correct',
                }

                entity_model = apps.get_model(
                    app_label = 'human_resources',
                    model_name = 'employee'
                )

                entity_model.context.update({
                    entity_model._meta.model_name: system_user
                })

                entity = entity_model.objects.create( **entity_kwargs )

                print( f'        Employee {entity.id}, created for user {user.username}' )

            except Exception as exc:
                print( f'        Error Occured processing user {user.username}, Employee was not created' )

        print(f'Completed processing current Centurion Users migration to an Employee Entity.')
    except Exception as exc:
        pass

    
