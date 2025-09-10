import datetime
import pytest

from django.core.exceptions import ObjectDoesNotExist

from itam.models.device import DeviceOperatingSystem



@pytest.fixture( scope = 'class')
def model_deviceoperatingsystem(clean_model_from_db):

    yield DeviceOperatingSystem

    clean_model_from_db(DeviceOperatingSystem)


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

        kwargs = kwargs_device.copy()
        kwargs.update({
            'name': 'dos' + random_str
        })

        device = model_device.objects.create(
            **kwargs
        )

        kwargs = kwargs_operatingsystemversion.copy()
        kwargs.update({
            'name': 'dos' + random_str
        })

        operating_system_version = model_operatingsystemversion.objects.create(
            **kwargs
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

        try:
            device.delete()
        except ObjectDoesNotExist:
            pass

        operating_system_version.delete()
