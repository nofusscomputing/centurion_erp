import pytest

from itam.models import ITAssetSoftware



@pytest.fixture( scope = 'class')
def model_itassetsoftware(clean_model_from_db):

    yield ITAssetSoftware

    # clean_model_from_db(ITAssetSoftware)


@pytest.fixture( scope = 'class')
def kwargs_itassetsoftware(django_db_blocker,
    kwargs_centurionmodel,
    model_itasset, kwargs_itasset,
    kwargs_softwareversion, model_softwareversion
):

    model_objs = []
    def factory(model_objs = model_objs):

        with django_db_blocker.unblock():

            itasset = model_itasset.objects.create(
                **kwargs_itasset()
            )

            softwareversion = model_softwareversion.objects.create(
                **kwargs_softwareversion()
            )

            model_objs += [ itasset, softwareversion ]

        kwargs = kwargs_centurionmodel()
        del kwargs['organization']

        kwargs = {
            **kwargs,
            'it_asset': itasset,
            'software': kwargs_softwareversion()['software'],
            'action': ITAssetSoftware.Actions.INSTALL,
            'version': softwareversion,
            'installedversion': softwareversion,
            'installed': '2025-06-11T17:38:00Z',
        }

        return kwargs

    yield factory
