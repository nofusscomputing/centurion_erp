import pytest



@pytest.fixture( scope = 'class')
def model(model_centurionmodelnote):

    yield model_centurionmodelnote


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_centurionmodelnote):

    request.cls.kwargs_create_item = kwargs_centurionmodelnote.copy()

    yield kwargs_centurionmodelnote.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
