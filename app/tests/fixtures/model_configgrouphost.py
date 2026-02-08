import pytest

from datetime import datetime

from config_management.models.groups import ConfigGroupHosts


@pytest.fixture( scope = 'class')
def model_configgrouphosts(clean_model_from_db):

    yield ConfigGroupHosts

    clean_model_from_db(ConfigGroupHosts)


@pytest.fixture( scope = 'class')
def kwargs_configgrouphosts(django_db_blocker,
    kwargs_device, model_device,
    kwargs_centurionmodel, model_configgroups, kwargs_configgroups,
):

    def factory():

        with django_db_blocker.unblock():

            centurion_kwargs = kwargs_centurionmodel()

            host = model_device.objects.create( **kwargs_device() )


            group_kwargs = kwargs_configgroups()
            group_kwargs.update({
                'name': 'cgg' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
                'organization': centurion_kwargs['organization']
            })

            group = model_configgroups.objects.create( **group_kwargs )

            host = model_device.objects.create( **kwargs_device() )

            kwargs = {
                **centurion_kwargs,
                'host': host,
                'group': group,
                }

        return kwargs

    yield factory
