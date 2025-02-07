# Generated by Django 5.1.5 on 2025-02-07 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_manufacturernotes'),
        ('project_management', '0006_projectstatenotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTypeNotes',
            fields=[
                ('modelnotes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelnotes')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='project_management.projecttype', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Project Type Note',
                'verbose_name_plural': 'Project Type Notes',
                'db_table': 'project_management_project_type_notes',
                'ordering': ['-created'],
            },
            bases=('core.modelnotes',),
        ),
    ]
