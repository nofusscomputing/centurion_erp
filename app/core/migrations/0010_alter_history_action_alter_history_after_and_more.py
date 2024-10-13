# Generated by Django 5.1.2 on 2024-10-13 15:27

import access.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_organization_id_alter_organization_manager_and_more'),
        ('config_management', '0006_alter_configgrouphosts_group_and_more'),
        ('core', '0009_alter_notes_options'),
        ('itam', '0014_alter_softwarecategory_options'),
        ('itim', '0005_alter_cluster_cluster_type_alter_cluster_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='action',
            field=models.IntegerField(choices=[('1', 'Create'), ('2', 'Update'), ('3', 'Delete')], default=None, help_text='History action performed', null=True, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='history',
            name='after',
            field=models.JSONField(blank=True, default=None, help_text='JSON Object After Change', null=True, verbose_name='After'),
        ),
        migrations.AlterField(
            model_name='history',
            name='before',
            field=models.JSONField(blank=True, default=None, help_text='JSON Object before Change', null=True, verbose_name='Before'),
        ),
        migrations.AlterField(
            model_name='history',
            name='id',
            field=models.AutoField(help_text='ID for this history entry', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='history',
            name='item_class',
            field=models.CharField(default=None, help_text='Class of the item this history relates to', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='item_parent_class',
            field=models.CharField(default=None, help_text='Class oof the Paarent Item this history relates to', max_length=50, null=True, verbose_name='Parent Class'),
        ),
        migrations.AlterField(
            model_name='history',
            name='item_parent_pk',
            field=models.IntegerField(default=None, help_text='Primary Key of the Parent Item this history relates to', null=True, verbose_name='Parent ID'),
        ),
        migrations.AlterField(
            model_name='history',
            name='item_pk',
            field=models.IntegerField(default=None, help_text='Primary Key of the item this history relates to', null=True, verbose_name='Item ID'),
        ),
        migrations.AlterField(
            model_name='history',
            name='user',
            field=models.ForeignKey(help_text='User whom performed the action this history relates to', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='id',
            field=models.AutoField(help_text='ID of the item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(help_text='Name of this manufacturer', max_length=50, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='config_group',
            field=models.ForeignKey(blank=True, default=None, help_text='Config group this note belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='config_management.configgroups', verbose_name='Config Group'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='device',
            field=models.ForeignKey(blank=True, default=None, help_text='Device this note belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.device', verbose_name='Device'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='id',
            field=models.AutoField(help_text='ID of this note', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='note',
            field=models.TextField(blank=True, default=None, help_text='The tid bit you wish to add', null=True, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='operatingsystem',
            field=models.ForeignKey(blank=True, default=None, help_text='Operating system this note belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.operatingsystem', verbose_name='Operating System'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='service',
            field=models.ForeignKey(blank=True, default=None, help_text='Service this note belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itim.service', verbose_name='Service'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='software',
            field=models.ForeignKey(blank=True, default=None, help_text='Software this note belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='itam.software', verbose_name='Software'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='usercreated',
            field=models.ForeignKey(blank=True, default=None, help_text='User whom added Note', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usercreated', to=settings.AUTH_USER_MODEL, verbose_name='Added By'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='usermodified',
            field=models.ForeignKey(blank=True, default=None, help_text='User whom modified the note', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='usermodified', to=settings.AUTH_USER_MODEL, verbose_name='Edited By'),
        ),
        migrations.AlterField(
            model_name='relatedtickets',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.AutoField(help_text='ID of the item', primary_key=True, serialize=False, unique=True, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcategory',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='ticketcategory',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='ticketcategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcomment',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcommentcategory',
            name='is_global',
            field=models.BooleanField(default=False, help_text='Is this a global object?', verbose_name='Global Object'),
        ),
        migrations.AlterField(
            model_name='ticketcommentcategory',
            name='model_notes',
            field=models.TextField(blank=True, default=None, help_text='Tid bits of information', null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='ticketcommentcategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketlinkeditem',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]