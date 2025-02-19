# Generated by Django 5.1.5 on 2025-02-15 12:10

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_team_organization_organizationnotes_teamnotes'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0014_data_move_notes_to_new_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelHistory',
            fields=[
                ('id', models.AutoField(help_text='ID of the item', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('is_global', models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object')),
                ('before', models.JSONField(blank=True, default=None, help_text='JSON Object before Change', null=True, verbose_name='Before')),
                ('after', models.JSONField(blank=True, default=None, help_text='JSON Object After Change', null=True, verbose_name='After')),
                ('action', models.IntegerField(choices=[(1, 'Create'), (2, 'Update'), (3, 'Delete')], default=None, help_text='History action performed', null=True, verbose_name='Action')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, help_text='Date and time of creation', verbose_name='Created')),
                ('content_type', models.ForeignKey(blank=True, help_text='Model this note is for', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content Model')),
                ('organization', models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization')),
                ('user', models.ForeignKey(help_text='User whom performed the action this history relates to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'History',
                'verbose_name_plural': 'History',
                'db_table': 'core_model_history',
                'ordering': ['-created'],
            },
        ),
    ]
