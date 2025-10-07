import pytest

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.serializers.software_enable_feature_flag import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_softwareenablefeatureflag(clean_model_from_db):

    yield SoftwareEnableFeatureFlag

    clean_model_from_db(SoftwareEnableFeatureFlag)


@pytest.fixture( scope = 'class')
def kwargs_softwareenablefeatureflag(django_db_blocker,
        kwargs_centurionmodel, model_software, kwargs_software
    ):

    def factory():

        with django_db_blocker.unblock():

            software = model_software.objects.create(
                **kwargs_software()
            )

        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']
        kwargs = {
            **kwargs,
            'software': software,
            'enabled': True
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_softwareenablefeatureflag():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
