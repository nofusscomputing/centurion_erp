import pytest



@pytest.fixture( scope = 'class')
def model(model_centurionmodelnotemeta):

    yield model_centurionmodelnotemeta


@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_centurionmodelnotemeta):

    request.cls.kwargs_create_item = kwargs_centurionmodelnotemeta()

    yield kwargs_centurionmodelnotemeta

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
