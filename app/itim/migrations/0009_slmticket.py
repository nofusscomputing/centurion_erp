# Generated by Django 5.1.8 on 2025-04-16 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_ticketcommentbase'),
        ('itim', '0008_clusterhistory_clustertypehistory_porthistory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SLMTicket',
            fields=[
                ('ticketbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ticketbase')),
                ('ttr', models.IntegerField(blank=True, default=0, help_text='Time taken to resolve the ticket / Time to Resolution (TTR)', verbose_name='TTR')),
                ('tto', models.IntegerField(blank=True, default=0, help_text='Time taken to Acknowledge ticket / Time to Ownership (TTO)', verbose_name='TTO')),
            ],
            options={
                'verbose_name': 'SLM Ticket Base',
                'verbose_name_plural': 'SLM Tickets',
                'ordering': ['id'],
            },
            bases=('core.ticketbase',),
        ),
    ]
