# Generated by Django 5.1.2 on 2024-11-20 02:41

import access.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0006_alter_team_organization'),
        ('core', '0015_alter_relatedtickets_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='relatedtickets',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcomment',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketcommentcategory',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='ticketlinkeditem',
            name='organization',
            field=models.ForeignKey(help_text='Organization this belongs to', on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists], verbose_name='Organization'),
        ),
    ]
