# Generated by Django 5.1.2 on 2024-10-17 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itam', '0015_alter_device_device_model_alter_device_device_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicesoftware',
            name='action',
            field=models.IntegerField(blank=True, choices=[(1, 'Install'), (0, 'Remove')], default=None, help_text='Action to perform', null=True, verbose_name='Action'),
        ),
    ]
