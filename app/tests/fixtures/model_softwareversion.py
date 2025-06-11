import datetime
import pytest

from itam.models.software import SoftwareVersion



@pytest.fixture( scope = 'class')
def model_softwareversion(request):

    yield SoftwareVersion


@pytest.fixture( scope = 'class')
def kwargs_softwareversion(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_software, model_software
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        software = model_software.objects.create( **kwargs_software )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'software': software,
        'name': 'softwareversion_' + random_str,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        software.delete()
