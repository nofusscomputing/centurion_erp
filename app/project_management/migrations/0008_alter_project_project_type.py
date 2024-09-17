# Generated by Django 5.0.8 on 2024-09-17 05:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0007_project_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.ForeignKey(blank=True, help_text='Type of project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.projecttype', verbose_name='Project Type'),
        ),
    ]
