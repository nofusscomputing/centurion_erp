# Generated by Django 5.1.2 on 2024-10-13 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config_management', '0004_alter_configgroups_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configgroupsoftware',
            options={'ordering': ['-action', 'software'], 'verbose_name': 'Config Group Software', 'verbose_name_plural': 'Config Group Softwares'},
        ),
    ]
