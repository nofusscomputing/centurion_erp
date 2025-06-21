import pytest



@pytest.fixture( scope = 'class')
def model(model_ticketcategory):

    yield model_ticketcategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcategory):

    request.cls.kwargs_create_item = kwargs_ticketcategory.copy()

    yield kwargs_ticketcategory.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
