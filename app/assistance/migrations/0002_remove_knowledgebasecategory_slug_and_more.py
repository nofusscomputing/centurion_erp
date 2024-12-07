# Generated by Django 5.1.2 on 2024-10-13 15:27

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_organization_id_alter_organization_manager_and_more'),
        ('assistance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgebasecategory',
            name='slug',
        ),
        migrations.AlterField(
            model_name='knowledgebase',
            name='id',
            field=models.AutoField(help_text='ID of this KB article', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='knowledgebase',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='knowledgebase',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='id',
            field=models.AutoField(help_text='ID of the item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]
