# Generated by Django 5.1.2 on 2024-11-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_alter_organization_options_alter_teamusers_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(help_text='Name to give this team', max_length=50, verbose_name='Name'),
        ),
    ]
