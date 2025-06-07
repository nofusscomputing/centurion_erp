import datetime
import pytest

from config_management.models.groups import ConfigGroupHosts


@pytest.fixture( scope = 'class')
def model_configgrouphosts():

    yield ConfigGroupHosts


@pytest.fixture( scope = 'class')
def kwargs_configgrouphosts(django_db_blocker,
    kwargs_device, model_device,
    kwargs_centurionmodel, model_configgroups, kwargs_configgroups,
):


    with django_db_blocker.unblock():

        centurion_kwargs = kwargs_centurionmodel.copy()

        random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

        host_kwargs = kwargs_device.copy()
        host_kwargs.update({
            'name': 'cgh' + str(random_str).replace(
                ' ', '').replace(':', '').replace('+', '').replace('.', ''),
            'organization': centurion_kwargs['organization']
        })

        host = model_device.objects.create( **host_kwargs )


        group_kwargs = kwargs_configgroups.copy()
        group_kwargs.update({
            'name': 'cgg' + random_str,
            'organization': centurion_kwargs['organization']
        })

        group = model_configgroups.objects.create( **group_kwargs )

        kwargs = {
            **centurion_kwargs,
            'host': host,
            'group': group,
            'modified': '2024-06-07T23:00:00Z',
            }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        host.delete()

        group.delete()
