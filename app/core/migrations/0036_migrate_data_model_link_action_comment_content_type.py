import django.db.models.deletion
import django.utils.timezone
import json

from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db import migrations, models



def migrate_data(apps, schema_editor):

    print('')
    print(f"Running migration for fix #1246")


    system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
        username = 'system'
    ).first()

    model_modelticket = apps.get_model(
        app_label = 'core',
        model_name = 'modelticket'
    )

    model_ticketcommentactionmodellink = apps.get_model(
        app_label = 'core',
        model_name = 'ticketcommentactionmodellink'
    )

    a = 'a'


    for row in model_ticketcommentactionmodellink.objects.all():

        row_model = apps.get_model(
            app_label = row.content_type.app_label,
            model_name = row.content_type.model
        )

        if not issubclass(row_model, model_modelticket): continue

        if not str(row.content_type.model).endswith('ticket'): continue

        print(f'    Starting migration of pk-{str(row.pk)} for ticket comment action model link.')

        # correct_row_model = apps.get_model(
        #     app_label = row.content_type.app_label,
        #     model_name = str(row.content_type.model)[0:(len(str(row.content_type.model)) - len('ticket'))]
        # )
        correct_row_model = type(row.content_type).objects.get(
            app_label = row.content_type.app_label,
            model = str(row.content_type.model)[0:(len(str(row.content_type.model)) - len('ticket'))]
        )

        # type(row).context.update({
        #     row._meta.model_name: system_user
        # })

        type(row).context = {
            row._meta.model_name: system_user
        }

        row.content_type = correct_row_model

        print(f'    Set correct model to app-{correct_row_model.app_label}, model-{correct_row_model.model}')

        row.save()

        print(f'    Updated database for pk-{str(row.pk)}')


        del type(row).context[row._meta.model_name]

    print(f'Migration Complete.')



class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_ticketcommentactionfieldedit_edit_type'),
    ]

    operations = [
        migrations.RunPython(migrate_data),
    ]
