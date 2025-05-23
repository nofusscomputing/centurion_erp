# Generated by Django 5.1.5 on 2025-02-20 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_modelhistory_manufacturerhistory_and_more'),
        ('settings', '0010_alter_usersettings_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettingsHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='settings.appsettings', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'App Settings History',
                'verbose_name_plural': 'App Settingsk History',
                'db_table': 'settings_appsettings_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='ExternalLinkHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='settings.externallink', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'External Link History',
                'verbose_name_plural': 'External Link History',
                'db_table': 'settings_externallink_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
    ]
