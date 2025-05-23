# Generated by Django 5.1.5 on 2025-02-20 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_modelhistory_manufacturerhistory_and_more'),
        ('itim', '0007_clusternotes_clustertypenotes_portnotes_servicenotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itim.cluster', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Cluster History',
                'verbose_name_plural': 'Cluster History',
                'db_table': 'itim_cluster_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='ClusterTypeHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itim.clustertype', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Cluster Type History',
                'verbose_name_plural': 'Cluster Type History',
                'db_table': 'itim_clustertype_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='PortHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itim.port', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Port History',
                'verbose_name_plural': 'Port History',
                'db_table': 'itim_port_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='ServiceHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itim.service', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Service History',
                'verbose_name_plural': 'Service History',
                'db_table': 'itim_service_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
    ]
