# Generated by Django 5.1.2 on 2024-10-16 06:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_organization_id_alter_organization_manager_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='teamusers',
            options={'ordering': ['user'], 'verbose_name': 'Team User', 'verbose_name_plural': 'Team Users'},
        ),
        migrations.AlterField(
            model_name='teamusers',
            name='id',
            field=models.AutoField(help_text='ID of this Team User', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teamusers',
            name='manager',
            field=models.BooleanField(blank=True, default=False, help_text='Is this user to be a manager of this team', verbose_name='manager'),
        ),
        migrations.AlterField(
            model_name='teamusers',
            name='team',
            field=models.ForeignKey(help_text='Team user belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='team', to='access.team', verbose_name='Team'),
        ),
        migrations.AlterField(
            model_name='teamusers',
            name='user',
            field=models.ForeignKey(help_text='User who will be added to the team', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
