# Generated by Django 5.1.5 on 2025-02-07 07:38

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0003_modelknowledgebasearticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgebase',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='modelknowledgebasearticle',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]
