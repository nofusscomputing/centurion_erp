# Generated by Django 5.1.2 on 2024-10-13 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_history_after_alter_history_before'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name'], 'verbose_name': 'Manufacturer', 'verbose_name_plural': 'Manufacturers'},
        ),
    ]
