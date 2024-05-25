# Generated by Django 5.0.6 on 2024-05-24 23:19

import access.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

from django.contrib.auth.models import User

from settings.models.user_settings import UserSettings

def add_user_settings(apps, schema_editor):

    for user in User.objects.all():

        if not UserSettings.objects.filter(pk=user.id).exists():

            user_setting = UserSettings.objects.create(
                user=user
            )

            user_setting.save()



class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_team_organization'),
        ('settings', '0002_usersettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(add_user_settings),
    ]
