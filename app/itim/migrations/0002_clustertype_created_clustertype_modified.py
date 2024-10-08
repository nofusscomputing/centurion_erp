# Generated by Django 5.0.7 on 2024-08-18 03:57

import access.fields
import django.utils.timezone
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itim', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustertype',
            name='created',
            field=access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='clustertype',
            name='modified',
            field=access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False),
        ),
    ]
