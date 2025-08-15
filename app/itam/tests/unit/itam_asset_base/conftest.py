import pytest



@pytest.fixture( scope = 'class')
def model(model_itamassetbase):

    yield model_itamassetbase


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itamassetbase):

    request.cls.kwargs_create_item = kwargs_itamassetbase.copy()

    yield kwargs_itamassetbase.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass
