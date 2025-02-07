# Generated by Django 5.1.5 on 2025-02-07 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_manufacturernotes'),
        ('itim', '0009_clustertypenotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortNotes',
            fields=[
                ('modelnotes_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelnotes')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='itim.port', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Port Note',
                'verbose_name_plural': 'Port Notes',
                'db_table': 'itim_port_notes',
                'ordering': ['-created'],
            },
            bases=('core.modelnotes',),
        ),
    ]
