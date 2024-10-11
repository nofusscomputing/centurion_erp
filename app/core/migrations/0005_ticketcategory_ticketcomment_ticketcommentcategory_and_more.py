# Generated by Django 5.0.8 on 2024-10-11 14:09

import access.fields
import access.models
import core.lib.slash_commands
import core.models.ticket.ticket
import core.models.ticket.ticket_comment
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
        ('core', '0004_notes_service'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketCategory',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(help_text='Category ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(help_text='Category Name', max_length=50, verbose_name='Name')),
                ('change', models.BooleanField(default=True, help_text='Use category for change tickets', verbose_name='Change Tickets')),
                ('incident', models.BooleanField(default=True, help_text='Use category for incident tickets', verbose_name='Incident Tickets')),
                ('problem', models.BooleanField(default=True, help_text='Use category for problem tickets', verbose_name='Problem Tickets')),
                ('project_task', models.BooleanField(default=True, help_text='Use category for Project tasks', verbose_name='Project Tasks')),
                ('request', models.BooleanField(default=True, help_text='Use category for request tickets', verbose_name='Request Tickets')),
            ],
            options={
                'verbose_name': 'Ticket Category',
                'verbose_name_plural': 'Ticket Categories',
                'ordering': ['parent__name', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TicketComment',
            fields=[
                ('id', models.AutoField(help_text='Comment ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('external_ref', models.IntegerField(blank=True, default=None, help_text='External System reference', null=True, verbose_name='Reference Number')),
                ('external_system', models.IntegerField(blank=True, choices=[(1, 'Github'), (2, 'Gitlab'), (9999, 'Custom #1 (Imported)'), (9998, 'Custom #2 (Imported)'), (9997, 'Custom #3 (Imported)'), (9996, 'Custom #4 (Imported)'), (9995, 'Custom #5 (Imported)'), (9994, 'Custom #6 (Imported)'), (9993, 'Custom #7 (Imported)'), (9992, 'Custom #8 (Imported)'), (9991, 'Custom #9 (Imported)')], default=None, help_text='External system this item derives', null=True, verbose_name='External System')),
                ('comment_type', models.IntegerField(choices=[(1, 'Action'), (2, 'Comment'), (3, 'Task'), (4, 'Notification'), (5, 'Solution')], default=2, help_text='The type of comment this is', validators=[core.models.ticket.ticket_comment.TicketComment.validation_comment_type], verbose_name='Type')),
                ('body', models.TextField(help_text='Comment contents', verbose_name='Comment')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('private', models.BooleanField(default=False, help_text='Is this comment private', verbose_name='Private')),
                ('duration', models.IntegerField(default=0, help_text='Time spent in seconds', verbose_name='Duration')),
                ('is_template', models.BooleanField(default=False, help_text='Is this comment a template', verbose_name='Template')),
                ('source', models.IntegerField(choices=[(1, 'Direct'), (2, 'E-Mail'), (3, 'Helpdesk'), (4, 'Phone')], default=1, help_text='Origin type for this comment', verbose_name='Source')),
                ('status', models.IntegerField(choices=[(1, 'To Do'), (2, 'Done')], default=1, help_text='Status of comment', verbose_name='Status')),
                ('date_closed', models.DateTimeField(blank=True, help_text='Date ticket closed', null=True, verbose_name='Closed Date')),
                ('planned_start_date', models.DateTimeField(blank=True, help_text='Planned start date.', null=True, verbose_name='Planned Start Date')),
                ('planned_finish_date', models.DateTimeField(blank=True, help_text='Planned finish date', null=True, verbose_name='Planned Finish Date')),
                ('real_start_date', models.DateTimeField(blank=True, help_text='Real start date', null=True, verbose_name='Real Start Date')),
                ('real_finish_date', models.DateTimeField(blank=True, help_text='Real finish date', null=True, verbose_name='Real Finish Date')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['ticket', 'parent_id'],
            },
            bases=(core.lib.slash_commands.SlashCommands, models.Model),
        ),
        migrations.CreateModel(
            name='TicketCommentCategory',
            fields=[
                ('is_global', models.BooleanField(default=False)),
                ('model_notes', models.TextField(blank=True, default=None, null=True, verbose_name='Notes')),
                ('id', models.AutoField(help_text='Category ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(help_text='Category Name', max_length=50, verbose_name='Name')),
                ('comment', models.BooleanField(default=True, help_text='Use category for standard comment', verbose_name='Comment')),
                ('notification', models.BooleanField(default=True, help_text='Use category for notification comment', verbose_name='Notification Comment')),
                ('solution', models.BooleanField(default=True, help_text='Use category for solution comment', verbose_name='Solution Comment')),
                ('task', models.BooleanField(default=True, help_text='Use category for task comment', verbose_name='Task Comment')),
            ],
            options={
                'verbose_name': 'Ticket Comment Category',
                'verbose_name_plural': 'Ticket Comment Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TicketLinkedItem',
            fields=[
                ('id', models.AutoField(help_text='ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('item_type', models.IntegerField(choices=[(1, 'Cluster'), (2, 'Config Group'), (3, 'Device'), (4, 'Operating System'), (5, 'Service'), (6, 'Software')], help_text='Python Model location for linked item', verbose_name='Item Type')),
                ('item', models.IntegerField(help_text='Item ID to link to ticket', verbose_name='Item ID')),
            ],
            options={
                'verbose_name': 'Ticket Linked Item',
                'verbose_name_plural': 'Ticket linked Items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RelatedTickets',
            fields=[
                ('id', models.AutoField(help_text='Ticket ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('how_related', models.IntegerField(choices=[(1, 'Related'), (2, 'Blocks'), (3, 'Blocked By')], help_text='How is the ticket related', verbose_name='How Related')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='access.organization', validators=[access.models.TenancyObject.validatate_organization_exists])),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(help_text='Ticket ID Number', primary_key=True, serialize=False, unique=True, verbose_name='Number')),
                ('created', access.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', access.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'New'), (3, 'Assigned'), (6, 'Assigned (Planning)'), (7, 'Pending'), (8, 'Solved'), (4, 'Closed'), (5, 'Invalid'), (10, 'Accepted'), (9, 'Under Observation'), (11, 'Evaluation'), (12, 'Approvals'), (13, 'Testing'), (14, 'Qualification'), (15, 'Applied'), (16, 'Review'), (17, 'Cancelled'), (18, 'Refused')], default=2, help_text='Status of ticket', verbose_name='Status')),
                ('title', models.CharField(help_text='Title of the Ticket', max_length=100, unique=True, verbose_name='Title')),
                ('description', models.TextField(help_text='Ticket Description', verbose_name='Description')),
                ('urgency', models.IntegerField(blank=True, choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very High')], default=1, help_text='How urgent is this tickets resolution for the user?', null=True, verbose_name='Urgency')),
                ('impact', models.IntegerField(blank=True, choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very High')], default=1, help_text='End user assessed impact', null=True, verbose_name='Impact')),
                ('priority', models.IntegerField(blank=True, choices=[(1, 'Very Low'), (2, 'Low'), (3, 'Medium'), (4, 'High'), (5, 'Very High'), (6, 'Major')], default=1, help_text='What priority should this ticket for its completion', null=True, verbose_name='Priority')),
                ('external_ref', models.IntegerField(blank=True, default=None, help_text='External System reference', null=True, verbose_name='Reference Number')),
                ('external_system', models.IntegerField(blank=True, choices=[(1, 'Github'), (2, 'Gitlab'), (9999, 'Custom #1 (Imported)'), (9998, 'Custom #2 (Imported)'), (9997, 'Custom #3 (Imported)'), (9996, 'Custom #4 (Imported)'), (9995, 'Custom #5 (Imported)'), (9994, 'Custom #6 (Imported)'), (9993, 'Custom #7 (Imported)'), (9992, 'Custom #8 (Imported)'), (9991, 'Custom #9 (Imported)')], default=None, help_text='External system this item derives', null=True, verbose_name='External System')),
                ('ticket_type', models.IntegerField(choices=[(1, 'Request'), (2, 'Incident'), (3, 'Change'), (4, 'Problem'), (5, 'Issue'), (6, 'Merge Request'), (7, 'Project Task')], help_text='The type of ticket this is', validators=[core.models.ticket.ticket.Ticket.validation_ticket_type], verbose_name='Type')),
                ('is_deleted', models.BooleanField(default=False, help_text='Is the ticket deleted? And ready to be purged', verbose_name='Deleted')),
                ('date_closed', models.DateTimeField(blank=True, help_text='Date ticket closed', null=True, verbose_name='Closed Date')),
                ('planned_start_date', models.DateTimeField(blank=True, help_text='Planned start date.', null=True, verbose_name='Planned Start Date')),
                ('planned_finish_date', models.DateTimeField(blank=True, help_text='Planned finish date', null=True, verbose_name='Planned Finish Date')),
                ('estimate', models.IntegerField(default=0, help_text='Time Eastimated to complete this ticket in seconds', verbose_name='Estimation')),
                ('real_start_date', models.DateTimeField(blank=True, help_text='Real start date', null=True, verbose_name='Real Start Date')),
                ('real_finish_date', models.DateTimeField(blank=True, help_text='Real finish date', null=True, verbose_name='Real Finish Date')),
                ('assigned_teams', models.ManyToManyField(blank=True, help_text='Assign the ticket to a Team(s)', related_name='assigned_teams', to='access.team', verbose_name='Assigned Team(s)')),
                ('assigned_users', models.ManyToManyField(blank=True, help_text='Assign the ticket to a User(s)', related_name='assigned_users', to=settings.AUTH_USER_MODEL, verbose_name='Assigned User(s)')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'ordering': ['id'],
                'permissions': [('add_ticket_request', 'Can add a request ticket'), ('change_ticket_request', 'Can change any request ticket'), ('delete_ticket_request', 'Can delete a request ticket'), ('import_ticket_request', 'Can import a request ticket'), ('purge_ticket_request', 'Can purge a request ticket'), ('triage_ticket_request', 'Can triage all request ticket'), ('view_ticket_request', 'Can view all request ticket'), ('add_ticket_incident', 'Can add a incident ticket'), ('change_ticket_incident', 'Can change any incident ticket'), ('delete_ticket_incident', 'Can delete a incident ticket'), ('import_ticket_incident', 'Can import a incident ticket'), ('purge_ticket_incident', 'Can purge a incident ticket'), ('triage_ticket_incident', 'Can triage all incident ticket'), ('view_ticket_incident', 'Can view all incident ticket'), ('add_ticket_problem', 'Can add a problem ticket'), ('change_ticket_problem', 'Can change any problem ticket'), ('delete_ticket_problem', 'Can delete a problem ticket'), ('import_ticket_problem', 'Can import a problem ticket'), ('purge_ticket_problem', 'Can purge a problem ticket'), ('triage_ticket_problem', 'Can triage all problem ticket'), ('view_ticket_problem', 'Can view all problem ticket'), ('add_ticket_change', 'Can add a change ticket'), ('change_ticket_change', 'Can change any change ticket'), ('delete_ticket_change', 'Can delete a change ticket'), ('import_ticket_change', 'Can import a change ticket'), ('purge_ticket_change', 'Can purge a change ticket'), ('triage_ticket_change', 'Can triage all change ticket'), ('view_ticket_change', 'Can view all change ticket'), ('add_ticket_project_task', 'Can add a project task'), ('change_ticket_project_task', 'Can change any project task'), ('delete_ticket_project_task', 'Can delete a project task'), ('import_ticket_project_task', 'Can import a project task'), ('purge_ticket_project_task', 'Can purge a project task'), ('triage_ticket_project_task', 'Can triage all project task'), ('view_ticket_project_task', 'Can view all project task')],
            },
            bases=(core.lib.slash_commands.SlashCommands, models.Model),
        ),
    ]
