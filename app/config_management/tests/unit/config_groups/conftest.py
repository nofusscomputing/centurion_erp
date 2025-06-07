import pytest



@pytest.fixture( scope = 'class')
def model(model_configgroups):

    yield model_configgroups


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_configgroups):

    request.cls.kwargs_create_item = kwargs_configgroups.copy()

    yield kwargs_configgroups.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
