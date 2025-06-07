import pytest

from core.models.centurion import CenturionSubModel



@pytest.fixture( scope = 'class')
def model(model_centurionsubmodel):

    yield model_centurionsubmodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionsubmodel):

    request.cls.kwargs_create_item = kwargs_centurionsubmodel.copy()

    yield kwargs_centurionsubmodel.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
