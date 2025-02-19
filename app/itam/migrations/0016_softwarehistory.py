# Generated by Django 5.1.5 on 2025-02-16 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_ticketcommentcategoryhistory'),
        ('itam', '0015_operatingsystemversionhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.software', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Software History',
                'verbose_name_plural': 'Software History',
                'db_table': 'itam_software_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
    ]
