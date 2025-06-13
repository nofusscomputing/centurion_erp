import datetime
import pytest

from config_management.models.groups import ConfigGroupSoftware

from itam.models.device import DeviceSoftware


@pytest.fixture( scope = 'class')
def model_configgroupsoftware():

    yield ConfigGroupSoftware


@pytest.fixture( scope = 'class')
def kwargs_configgroupsoftware(django_db_blocker,
    kwargs_software, model_software,
    kwargs_centurionmodel, model_configgroups, kwargs_configgroups,
):


    with django_db_blocker.unblock():

        centurion_kwargs = kwargs_centurionmodel.copy()

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        software_kwargs = kwargs_software.copy()
        software_kwargs.update({
            'name': 'cgs' + str(random_str),
            'organization': centurion_kwargs['organization']
        })

        software = model_software.objects.create( **software_kwargs )


        group_kwargs = kwargs_configgroups.copy()
        group_kwargs.update({
            'name': 'cgg' + random_str,
            'organization': centurion_kwargs['organization']
        })

        group = model_configgroups.objects.create( **group_kwargs )

        kwargs = {
            **centurion_kwargs,
            'software': software,
            'config_group': group,
            'action': DeviceSoftware.Actions.INSTALL,
            'modified': '2024-06-07T23:00:01Z',
            }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        software.delete()

        group.delete()
