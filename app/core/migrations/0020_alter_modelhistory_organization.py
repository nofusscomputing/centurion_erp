# Generated by Django 5.1.5 on 2025-02-20 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0004_organizationhistory_teamhistory'),
        ('core', '0019_data_move_history_to_new_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelhistory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='access.organization', verbose_name='Organization'),
        ),
    ]
