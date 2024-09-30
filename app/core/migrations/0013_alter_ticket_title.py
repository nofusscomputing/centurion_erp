# Generated by Django 5.0.8 on 2024-09-30 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_ticket_estimate_alter_ticket_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(help_text='Title of the Ticket', max_length=100, unique=True, verbose_name='Title'),
        ),
    ]
