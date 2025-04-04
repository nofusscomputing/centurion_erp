# Generated by Django 5.1.5 on 2025-02-09 11:07

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_team_organization_organizationnotes_teamnotes'),
        ('assistance', '0003_modelknowledgebasearticle'),
        ('core', '0012_modelnotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgebase',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='knowledgebasecategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='modelknowledgebasearticle',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', validators=[access.models.tenancy.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.CreateModel(
            name='KnowledgeBaseNotes',
            fields=[
                ('modelnotes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelnotes')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='assistance.knowledgebase', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Knowledge Base Note',
                'verbose_name_plural': 'Knowledge Base Notes',
                'db_table': 'assistance_knowledge_base_notes',
                'ordering': ['-created'],
            },
            bases=('core.modelnotes',),
        ),
        migrations.CreateModel(
            name='KnowledgeCategoryBaseNotes',
            fields=[
                ('modelnotes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelnotes')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='assistance.knowledgebasecategory', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Knowledge Base Category Note',
                'verbose_name_plural': 'Knowledge Base Category Notes',
                'db_table': 'assistance_knowledge_base_category_notes',
                'ordering': ['-created'],
            },
            bases=('core.modelnotes',),
        ),
    ]
