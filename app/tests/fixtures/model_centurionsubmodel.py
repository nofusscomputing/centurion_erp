import pytest

from core.models.centurion import CenturionSubModel



@pytest.fixture( scope = 'class')
def model_centurionsubmodel(request):

    yield CenturionSubModel


@pytest.fixture( scope = 'class')
def kwargs_centurionsubmodel(request, kwargs_centurionmodel):

    kwargs = {
        **kwargs_centurionmodel.copy(),
    }

    yield kwargs.copy()
