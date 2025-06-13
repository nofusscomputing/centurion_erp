import pytest



@pytest.fixture( scope = 'class')
def model(model_softwarecategory):

    yield model_softwarecategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_softwarecategory):

    request.cls.kwargs_create_item = kwargs_softwarecategory.copy()

    yield kwargs_softwarecategory.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
