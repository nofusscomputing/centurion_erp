import pytest

from datetime import datetime

from core.models.ticket_base import TicketBase
from core.serializers.ticketbase import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketbase(clean_model_from_db):

    yield TicketBase

    clean_model_from_db(TicketBase)


@pytest.fixture( scope = 'class')
def kwargs_ticketbase(django_db_blocker, kwargs_centurionmodel,
    model_user, kwargs_user, model_ticketbase,
    model_employee, kwargs_employee,
    model_project, model_projectmilestone,
    model_ticketcategory,
):


    def factory():

        random_str = str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

        with django_db_blocker.unblock():

            kwargs = kwargs_employee()
            kwargs['f_name'] = 'tb_fn_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

            user = model_employee.objects.create( **kwargs )


            project = model_project.objects.create(
                organization = kwargs_centurionmodel()['organization'],
                name = 'project_ticket' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )
            )

            project_milestone = model_projectmilestone.objects.create(
                organization = kwargs_centurionmodel()['organization'],
                name = 'project milestone one' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
                project = project
            )

            category = model_ticketcategory.objects.create(
                organization = kwargs_centurionmodel()['organization'],
                name = 'tb cat ' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            )


        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        kwargs = {
            **kwargs,


            'category': category,
            'opened_by': user,
            'project': project,
            'milestone': project_milestone,
            # 'parent_ticket': None,
            'external_system': model_ticketbase.Ticket_ExternalSystem.GITHUB,
            'external_ref': int(random_str),
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

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketbase():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
