# Generated by Django 5.1.5 on 2025-02-08 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistance', '0006_alter_knowledgebasenotes_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='knowledgecategorybasenotes',
            options={'ordering': ['-created'], 'verbose_name': 'Knowledge Base Category Note', 'verbose_name_plural': 'Knowledge Base Category Notes'},
        ),
    ]
