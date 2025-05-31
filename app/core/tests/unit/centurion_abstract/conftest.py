import pytest



@pytest.fixture( scope = 'class')
def model(model_centurionmodel):

    yield model_centurionmodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionmodel):

    request.cls.kwargs_create_item = kwargs_centurionmodel.copy()

    yield kwargs_centurionmodel.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
