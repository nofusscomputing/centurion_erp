import pytest

from itam.models.device import DeviceSoftware



@pytest.fixture( scope = 'class')
def model_devicesoftware(clean_model_from_db):

    yield DeviceSoftware

    clean_model_from_db(DeviceSoftware)


@pytest.fixture( scope = 'class')
def kwargs_devicesoftware(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_device, model_device,
    kwargs_softwareversion, model_softwareversion
):

    model_objs = []
    def factory(model_objs = model_objs):

        with django_db_blocker.unblock():

            device = model_device.objects.create(
                **kwargs_device()
            )

            softwareversion = model_softwareversion.objects.create(
                **kwargs_softwareversion()
            )

            model_objs += [ device, softwareversion ]

        kwargs = {
            **kwargs_centurionmodel(),
            'device': device,
            'software': kwargs_softwareversion()['software'],
            'action': DeviceSoftware.Actions.INSTALL,
            'version': softwareversion,
            'installedversion': softwareversion,
            'installed': '2025-06-11T17:38:00Z',
        }

        return kwargs

    yield factory
