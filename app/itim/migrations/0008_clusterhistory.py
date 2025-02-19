# Generated by Django 5.1.5 on 2025-02-16 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_ticketcommentcategoryhistory'),
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
    ]
