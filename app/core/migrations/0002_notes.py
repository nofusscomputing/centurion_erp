# Generated by Django 5.0.7 on 2024-07-12 03:58

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
        ('config_management', '0002_configgrouphosts_configgroupsoftware'),
        ('core', '0001_initial'),
        ('itam', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('note', models.TextField(blank=True, default=None, null=True, verbose_name='Note')),
                ('config_group', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='config_management.configgroups')),
                ('device', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.device')),
                ('operatingsystem', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.operatingsystem')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists])),
                ('software', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.software')),
                ('usercreated', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='usercreated', to=settings.AUTH_USER_MODEL, verbose_name='Added By')),
                ('usermodified', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='usermodified', to=settings.AUTH_USER_MODEL, verbose_name='Edited By')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
