import datetime
import pytest

from itam.models.device import DeviceSoftware



@pytest.fixture( scope = 'class')
def model_devicesoftware():

    yield DeviceSoftware


@pytest.fixture( scope = 'class')
def kwargs_devicesoftware(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_device, model_device,
    kwargs_softwareversion, model_softwareversion
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        device = model_device.objects.create(
            **kwargs_device.copy()
        )

        softwareversion = model_softwareversion.objects.create(
            **kwargs_softwareversion
        )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'device': device,
        'software': kwargs_softwareversion['software'],
        'action': DeviceSoftware.Actions.INSTALL,
        'version': softwareversion,
        'installedversion': softwareversion,
        'installed': '2025-06-11T17:38:00Z',
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        device.delete()

        softwareversion.delete()
