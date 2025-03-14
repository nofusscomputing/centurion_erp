# Generated by Django 5.1.5 on 2025-03-14 15:26

import access.fields
import access.models.tenancy
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_organizationhistory_teamhistory'),
        ('devops', '0007_alter_featureflag_software'),
        ('itam', '0010_alter_software_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(help_text='Primary key of the entry', primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('deployment_id', models.CharField(help_text='Unique Deployment ID', max_length=64, verbose_name='Deployment ID')),
                ('feature', models.TextField(help_text='Feature that was checked into', max_length=30, verbose_name='Feature')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, help_text='Date and time of creation', verbose_name='Created')),
                ('organization', models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization')),
                ('software', models.ForeignKey(help_text='Software related to the checkin', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='itam.software', verbose_name='Software')),
            ],
            options={
                'verbose_name': 'Deployment Check In',
                'verbose_name_plural': 'Deployment Check Ins',
                'ordering': ['organization', 'software', 'feature'],
            },
        ),
    ]
