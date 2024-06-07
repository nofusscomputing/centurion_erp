# Generated by Django 5.0.6 on 2024-06-07 21:43

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_team_organization'),
        ('config_management', '0003_alter_configgrouphosts_organization_and_more'),
        ('itam', '0013_alter_device_organization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigGroupSoftware',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('action', models.CharField(blank=True, choices=[('1', 'Install'), ('0', 'Remove')], default=None, max_length=1, null=True)),
                ('config_group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='config_management.configgroups')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
                ('software', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='itam.software')),
                ('version', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.softwareversion')),
            ],
            options={
                'ordering': ['-action', 'software'],
            },
        ),
    ]
