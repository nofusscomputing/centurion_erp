import pytest

from devops.models.feature_flag import FeatureFlag
from devops.serializers.feature_flag import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_featureflag(clean_model_from_db):

    yield FeatureFlag

    clean_model_from_db(FeatureFlag)


@pytest.fixture( scope = 'class')
def kwargs_featureflag(django_db_blocker, kwargs_centurionmodel, model_software, kwargs_software, model_softwareenablefeatureflag):


    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_software()

            # kwargs.update({'name': 'ff_enable_software'})

            software = model_software.objects.create(
                **kwargs
            )

            enable_feature_flag = model_softwareenablefeatureflag.objects.create(
                organization = kwargs_centurionmodel()['organization'],
                software = software,
                enabled = True
            )

            kwargs = {
                **kwargs_centurionmodel(),
                'software': software,
                'name': 'a name',
                'description': ' a description',
                'enabled': True,
            }

        return kwargs

    yield factory




@pytest.fixture( scope = 'class')
def serializer_featureflag():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
