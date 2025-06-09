import datetime
import pytest

from devops.models.check_ins import CheckIn



@pytest.fixture( scope = 'class')
def model_checkin():

    yield CheckIn


@pytest.fixture( scope = 'class')
def kwargs_checkin(django_db_blocker,
    kwargs_centurionmodel, model_software
):


    with django_db_blocker.unblock():

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        software = model_software.objects.create(
            organization = kwargs_centurionmodel['organization'],
            name = 'ci' + random_str
        )

        kwargs = {
            **kwargs_centurionmodel.copy(),
            'software': software,
            'version': '1.20.300',
            'deployment_id': 'rand deploymentid',
            'feature': 'a feature',
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        software.delete()
