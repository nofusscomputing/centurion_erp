import datetime
import pytest

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag



@pytest.fixture( scope = 'class')
def model_softwareenablefeatureflag(request):

    yield SoftwareEnableFeatureFlag


@pytest.fixture( scope = 'class')
def kwargs_softwareenablefeatureflag(django_db_blocker,
        kwargs_centurionmodel, model_software, kwargs_software
    ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        kwargs_soft = kwargs_software.copy()
        kwargs_soft.update({
            'name': 'seff' + str(random_str).replace(
                ' ', '').replace(':', '').replace('+', '').replace('.', '')
        })

        software = model_software.objects.create(
            **kwargs_soft
        )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'software': software,
        'enabled': True
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        software.delete()
