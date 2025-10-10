import pytest

from devops.models.check_ins import CheckIn



@pytest.fixture( scope = 'class')
def model_checkin(clean_model_from_db):

    yield CheckIn

    clean_model_from_db(CheckIn)


@pytest.fixture( scope = 'class')
def kwargs_checkin(django_db_blocker,
    kwargs_centurionmodel, kwargs_featureflag
):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'software': kwargs_featureflag()['software'],
            'version': '1.20.300',
            'deployment_id': 'rand deploymentid',
            'feature': 'a feature',
        }

        return kwargs

    yield factory
