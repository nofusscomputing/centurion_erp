# Generated by Django 5.1.2 on 2024-10-24 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_appsettings_device_model_is_global_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appsettings',
            options={'ordering': ['owner_organization'], 'verbose_name': 'App Settings', 'verbose_name_plural': 'App Settings'},
        ),
    ]