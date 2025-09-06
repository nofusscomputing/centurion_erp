import pytest



@pytest.fixture( scope = 'class')
def model(model_configgroupsoftware):

    yield model_configgroupsoftware


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_configgroupsoftware):

    request.cls.kwargs_create_item = kwargs_configgroupsoftware.copy()

    yield kwargs_configgroupsoftware.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
