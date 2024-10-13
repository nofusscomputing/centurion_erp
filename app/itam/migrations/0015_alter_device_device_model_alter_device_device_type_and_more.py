# Generated by Django 5.1.2 on 2024-10-13 15:27

import access.models
import django.db.models.deletion
import itam.models.device
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_organization_id_alter_organization_manager_and_more'),
        ('itam', '0014_alter_softwarecategory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_model',
            field=models.ForeignKey(blank=True, default=None, help_text='Model of the device.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='itam.devicemodel', verbose_name='Model'),
        ),
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(blank=True, default=None, help_text='Type of device.', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='itam.devicetype', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='device',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='device',
            name='inventorydate',
            field=models.DateTimeField(blank=True, help_text='Date and time of the last inventory', null=True, verbose_name='Last Inventory Date'),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='device',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(help_text='Hostname of this device', max_length=50, unique=True, validators=[itam.models.device.Device.validate_hostname_format], verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='device',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='manufacturer',
            field=models.ForeignKey(blank=True, default=None, help_text='Manufacturer this model is from', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.manufacturer', verbose_name='Manufacturer'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='name',
            field=models.CharField(help_text='The items name', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='devicemodel',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='device',
            field=models.ForeignKey(help_text='Device for the Operating System', on_delete=django.db.models.deletion.CASCADE, to='itam.device', verbose_name='Device'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='installdate',
            field=models.DateTimeField(blank=True, default=None, help_text='Date and time detected as installed', null=True, verbose_name='Install Date'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='operating_system_version',
            field=models.ForeignKey(help_text='Operating system version', on_delete=django.db.models.deletion.CASCADE, to='itam.operatingsystemversion', verbose_name='Operating System/Version'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='deviceoperatingsystem',
            name='version',
            field=models.CharField(help_text='Version detected as installed', max_length=15, verbose_name='Installed Version'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='device',
            field=models.ForeignKey(help_text='Device this software is on', on_delete=django.db.models.deletion.CASCADE, to='itam.device', verbose_name='Device'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='installedversion',
            field=models.ForeignKey(blank=True, default=None, help_text='Version that is installed', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='installedversion', to='itam.softwareversion', verbose_name='Installed Version'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='devicesoftware',
            name='software',
            field=models.ForeignKey(help_text='Software Name', on_delete=django.db.models.deletion.CASCADE, to='itam.software', verbose_name='Software'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='name',
            field=models.CharField(help_text='The items name', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='devicetype',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='name',
            field=models.CharField(help_text='Name of this item', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='operatingsystem',
            name='publisher',
            field=models.ForeignKey(blank=True, default=None, help_text='Who publishes this Operating System', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.manufacturer', verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='id',
            field=models.AutoField(help_text='ID of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='name',
            field=models.CharField(help_text='Major version number for the Operating System', max_length=50, verbose_name='Major Version'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='operating_system',
            field=models.ForeignKey(help_text='Operating system this version applies to', on_delete=django.db.models.deletion.CASCADE, to='itam.operatingsystem', verbose_name='Operaating System'),
        ),
        migrations.AlterField(
            model_name='operatingsystemversion',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='software',
            name='category',
            field=models.ForeignKey(blank=True, default=None, help_text='Category of this Softwarae', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='itam.softwarecategory', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='software',
            name='id',
            field=models.AutoField(help_text='Id of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='software',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='software',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='software',
            name='name',
            field=models.CharField(help_text='Name of this item', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='software',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='software',
            name='publisher',
            field=models.ForeignKey(blank=True, default=None, help_text='Who publishes this software', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.manufacturer', verbose_name='Publisher'),
        ),
        migrations.AlterField(
            model_name='softwarecategory',
            name='id',
            field=models.AutoField(help_text='Id of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='softwarecategory',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='softwarecategory',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='softwarecategory',
            name='name',
            field=models.CharField(help_text='Name of this item', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='softwarecategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='id',
            field=models.AutoField(help_text='Id of this item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='name',
            field=models.CharField(help_text='Name of for the software version', max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='software',
            field=models.ForeignKey(help_text='Software this version applies', on_delete=django.db.models.deletion.CASCADE, to='itam.software', verbose_name='Software'),
        ),
    ]