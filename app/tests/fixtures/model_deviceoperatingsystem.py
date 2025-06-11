import datetime
import pytest

from itam.models.device import DeviceOperatingSystem



@pytest.fixture( scope = 'class')
def model_deviceoperatingsystem():

    yield DeviceOperatingSystem


@pytest.fixture( scope = 'class')
def kwargs_deviceoperatingsystem(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_device, model_device,
    kwargs_operatingsystemversion, model_operatingsystemversion
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        device = model_device.objects.create(
            **kwargs_device.copy()
        )

        operating_system_version = model_operatingsystemversion.objects.create(
            **kwargs_operatingsystemversion.copy()
        )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'device': device,
        'operating_system_version': operating_system_version,
        'version': 'devos' + str(random_str)[len(str(random_str))-10:],
        'installdate': '2025-06-11T17:38:00Z',
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        device.delete()

        operating_system_version.delete()
