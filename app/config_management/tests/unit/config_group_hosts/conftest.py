import pytest



@pytest.fixture( scope = 'class')
def model(model_configgrouphost):

    yield model_configgrouphost


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_configgrouphost):

    request.cls.kwargs_create_item = kwargs_configgrouphost.copy()

    yield kwargs_configgrouphost.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
