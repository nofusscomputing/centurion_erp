import pytest



@pytest.fixture( scope = 'class')
def model(model_ticketcommentcategory):

    yield model_ticketcommentcategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentcategory):

    request.cls.kwargs_create_item = kwargs_ticketcommentcategory()

    yield kwargs_ticketcommentcategory

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentcategory):

    yield serializer_ticketcommentcategory

