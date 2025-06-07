import pytest



@pytest.fixture( scope = 'class')
def model(model_configgroup):

    yield model_configgroup


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_configgroup):

    request.cls.kwargs_create_item = kwargs_configgroup.copy()

    yield kwargs_configgroup.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
