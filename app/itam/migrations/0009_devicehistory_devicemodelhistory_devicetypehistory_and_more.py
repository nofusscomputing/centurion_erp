# Generated by Django 5.1.5 on 2025-02-20 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_modelhistory_manufacturerhistory_and_more'),
        ('itam', '0008_alter_device_organization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.device', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Device History',
                'verbose_name_plural': 'Device History',
                'db_table': 'itam_device_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='DeviceModelHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.devicemodel', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Device Model History',
                'verbose_name_plural': 'Device Model History',
                'db_table': 'itam_devicemodel_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='DeviceTypeHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.devicetype', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Device Type History',
                'verbose_name_plural': 'Device TYpe History',
                'db_table': 'itam_devicetype_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='OperatingSystemHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.operatingsystem', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Operating System History',
                'verbose_name_plural': 'Operating System History',
                'db_table': 'itam_operatingsystem_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='OperatingSystemVersionHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.operatingsystemversion', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Operating System Version History',
                'verbose_name_plural': 'Operating Version System History',
                'db_table': 'itam_operatingsystemversion_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='SoftwareCategoryHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.softwarecategory', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Software Category History',
                'verbose_name_plural': 'Software Category History',
                'db_table': 'itam_softwarecategory_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
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
        migrations.CreateModel(
            name='SoftwareVersionHistory',
            fields=[
                ('modelhistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.modelhistory')),
                ('model', models.ForeignKey(help_text='Model this note belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='history', to='itam.softwareversion', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Software Version History',
                'verbose_name_plural': 'Software Version History',
                'db_table': 'itam_softwareversion_history',
                'ordering': ['-created'],
            },
            bases=('core.modelhistory',),
        ),
        migrations.CreateModel(
            name='DeviceOperatingSystemHistory',
            fields=[
                ('devicehistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='itam.devicehistory')),
                ('child_model', models.ForeignKey(help_text='Model this note belongs to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='itam.deviceoperatingsystem', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Device Operating System History',
                'verbose_name_plural': 'Device Operating System History',
                'db_table': 'itam_deviceoperatingsystem_history',
                'ordering': ['-created'],
            },
            bases=('itam.devicehistory',),
        ),
        migrations.CreateModel(
            name='DeviceSoftwareHistory',
            fields=[
                ('devicehistory_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='itam.devicehistory')),
                ('child_model', models.ForeignKey(help_text='Model this note belongs to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='itam.devicesoftware', verbose_name='Model')),
            ],
            options={
                'verbose_name': 'Device Software History',
                'verbose_name_plural': 'Device Software History',
                'db_table': 'itam_devicesoftware_history',
                'ordering': ['-created'],
            },
            bases=('itam.devicehistory',),
        ),
    ]
