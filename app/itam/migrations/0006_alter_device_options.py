# Generated by Django 5.1.2 on 2024-10-13 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itam', '0005_alter_devicesoftware_action_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['name', 'organization'], 'verbose_name': 'Device', 'verbose_name_plural': 'Devices'},
        ),
    ]