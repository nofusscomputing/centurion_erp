# Generated by Django 5.1.2 on 2024-10-19 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_history_options_alter_history_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='note',
            field=models.TextField(default='-', help_text='The tid bit you wish to add', verbose_name='Note'),
            preserve_default=False,
        ),
    ]
