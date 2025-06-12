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
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        kwargs = kwargs_software
        kwargs.update({
            'name': 'sv_' + random_str
        })

        software = model_software.objects.create( **kwargs_software )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'software': software,
        'name': 'softwareversion_' + random_str,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        software.delete()
