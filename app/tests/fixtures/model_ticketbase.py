import datetime
import pytest
import random

from django.db import models

from core.models.ticket_base import TicketBase



@pytest.fixture( scope = 'class')
def model_ticketbase(clean_model_from_db):

    yield TicketBase

    clean_model_from_db(TicketBase)


@pytest.fixture( scope = 'class')
def kwargs_ticketbase(django_db_blocker, kwargs_centurionmodel,
    model_user, kwargs_user, model_ticketbase,
    model_project, model_projectmilestone,
    model_ticketcategory,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        user = model_user.objects.create( **kwargs_user.copy() )


        project = model_project.objects.create(
            organization = kwargs_centurionmodel['organization'],
            name = 'project' + str( random.randint(1, 99999))
        )

        project_milestone = model_projectmilestone.objects.create(
            organization = kwargs_centurionmodel['organization'],
            name = 'project milestone one' + str( random.randint(1, 99999)),
            project = project
        )

        category = model_ticketcategory.objects.create(
            organization = kwargs_centurionmodel['organization'],
            name = 'tb cat ' + str( random.randint(1, 99999)),
        )


    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,


        'category': category,
        'opened_by': user,
        'project': project,
        'milestone': project_milestone,
        # 'parent_ticket': None,
        'external_system': model_ticketbase.Ticket_ExternalSystem.GITHUB,
        'external_ref': int(random_str[len(random_str)-9:]),
        'impact': int(model_ticketbase.TicketImpact.MEDIUM),
        'priority': int(model_ticketbase.TicketPriority.HIGH),
        'status': model_ticketbase.TicketStatus.NEW,



        'title': 'tb_' + random_str,
        'description': 'the body',
        'planned_start_date': '2025-04-16T00:00:01Z',
        'planned_finish_date': '2025-04-16T00:00:02Z',
        'real_start_date': '2025-04-16T00:00:03Z',
        'real_finish_date': '2025-04-16T00:00:04Z',
        # 'is_solved': True,
        # 'date_solved': '2025-05-12T02:30:01',
        # 'is_closed': True,
        # 'date_closed': '2025-05-12T02:30:02',


    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            user.delete()
        except:
            pass

        try:
            project_milestone.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            project.delete()
        except models.deletion.ProtectedError:
            pass

        try:
            category.delete()
        except models.deletion.ProtectedError:
            pass
