import pytest



@pytest.fixture( scope = 'class')
def model(model_configgrouphosts):

    yield model_configgrouphosts


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_configgrouphosts):

    request.cls.kwargs_create_item = kwargs_configgrouphosts.copy()

    yield kwargs_configgrouphosts.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
