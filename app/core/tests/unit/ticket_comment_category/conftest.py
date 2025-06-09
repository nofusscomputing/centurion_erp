import pytest



@pytest.fixture( scope = 'class')
def model(model_ticketcommentcategory):

    yield model_ticketcommentcategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentcategory):

    request.cls.kwargs_create_item = kwargs_ticketcommentcategory.copy()

    yield kwargs_ticketcommentcategory.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
