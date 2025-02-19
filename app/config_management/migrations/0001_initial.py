# Generated by Django 5.0.7 on 2024-07-12 03:54

import access.fields
import access.models
import config_management.models.groups
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGroups',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('config', models.JSONField(blank=True, default=None, null=True, validators=[config_management.models.groups.ConfigGroups.validate_config_keys_not_reserved])),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists])),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='config_management.configgroups')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
