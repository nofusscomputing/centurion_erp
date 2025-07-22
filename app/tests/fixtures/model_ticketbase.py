import datetime
import pytest

from core.models.ticket_base import TicketBase



@pytest.fixture( scope = 'class')
def model_ticketbase(request):

    yield TicketBase


@pytest.fixture( scope = 'class')
def kwargs_ticketbase(django_db_blocker, kwargs_centurionmodel,
    model_user, kwargs_user, model_ticketbase
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        user = model_user.objects.create( **kwargs_user.copy() )

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        'external_system': model_ticketbase.Ticket_ExternalSystem.GITHUB,
        'external_ref': int(random_str[len(random_str)-9:]),
        'title': 'tb_' + random_str,
        'description': 'the body',
        'opened_by': user,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            user.delete()
        except:
            pass