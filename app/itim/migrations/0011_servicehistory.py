# Generated by Django 5.1.5 on 2025-02-16 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_ticketcommentcategoryhistory'),
        ('itim', '0010_porthistory'),
    ]

    operations = [
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
