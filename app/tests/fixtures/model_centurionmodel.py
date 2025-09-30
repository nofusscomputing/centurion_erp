import pytest

from core.models.centurion import CenturionModel



@pytest.fixture( scope = 'class')
def model_centurionmodel():

    yield CenturionModel


@pytest.fixture( scope = 'class')
def kwargs_centurionmodel(kwargs_tenancyabstract):

    def factory():

        kwargs = {
            **kwargs_tenancyabstract(),
            'model_notes': 'model notes txt',
            'created': '2025-05-23T00:00Z',
        }

        return kwargs

    yield factory
