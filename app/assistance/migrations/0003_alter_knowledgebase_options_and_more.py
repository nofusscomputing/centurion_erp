# Generated by Django 5.1.2 on 2024-10-16 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0002_remove_knowledgebasecategory_slug_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='knowledgebase',
            options={'ordering': ['title'], 'verbose_name': 'Knowledge Base', 'verbose_name_plural': 'Knowledge Base Articles'},
        ),
        migrations.AlterModelOptions(
            name='knowledgebasecategory',
            options={'ordering': ['name'], 'verbose_name': 'Knowledge Base Category', 'verbose_name_plural': 'Knowledge Base Categories'},
        ),
    ]
