# Generated by Django 5.1.5 on 2025-03-04 14:58

import access.models.tenancy
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_organizationhistory_teamhistory'),
        ('itam', '0009_devicehistory_devicemodelhistory_devicetypehistory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='software', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]
