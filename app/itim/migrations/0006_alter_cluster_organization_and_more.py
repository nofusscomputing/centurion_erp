# Generated by Django 5.1.5 on 2025-02-07 07:38

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itim', '0005_alter_port_options_alter_cluster_cluster_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='clustertype',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='port',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='service',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]
