# Generated by Django 5.0.7 on 2024-07-17 05:02

import access.fields
import access.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(help_text='Name to display on link button', max_length=30, unique=True, verbose_name='Button Name')),
                ('template', models.CharField(help_text='External Link template', max_length=180, verbose_name='Link Template')),
                ('colour', models.CharField(blank=True, default=None, help_text='Colour to render the link button. Use HTML colour code', max_length=80, null=True, verbose_name='Button Colour')),
                ('devices', models.BooleanField(default=False, help_text='Render link for devices', verbose_name='Devices')),
                ('software', models.BooleanField(default=False, help_text='Render link for software', verbose_name='Software')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
