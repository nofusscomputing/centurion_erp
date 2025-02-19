# Generated by Django 5.0.7 on 2024-07-12 03:54

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access', '0001_initial'),
        ('config_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('before', models.TextField(blank=True, default=None, help_text='JSON Object before Change', null=True)),
                ('after', models.TextField(blank=True, default=None, help_text='JSON Object After Change', null=True)),
                ('action', models.IntegerField(choices=[('1', 'Create'), ('2', 'Update'), ('3', 'Delete')], default=None, null=True)),
                ('item_pk', models.IntegerField(default=None, null=True)),
                ('item_class', models.CharField(default=None, max_length=50, null=True)),
                ('item_parent_pk', models.IntegerField(default=None, null=True)),
                ('item_parent_class', models.CharField(default=None, max_length=50, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', access.fields.AutoSlugField()),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
