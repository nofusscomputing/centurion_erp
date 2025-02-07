# Generated by Django 5.1.5 on 2025-02-07 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_organizationnotes'),
        ('core', '0013_alter_manufacturer_organization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamNotes',
            fields=[
                ('modelnotes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelnotes')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='access.team', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Team Note',
                'verbose_name_plural': 'Team Notes',
                'db_table': 'access_team_notes',
                'ordering': ['-created'],
            },
            bases=('core.modelnotes',),
        ),
    ]
