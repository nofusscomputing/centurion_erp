import pytest



@pytest.fixture( scope = 'class')
def model(model_knowledgebasecategory):

    yield model_knowledgebasecategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_knowledgebasecategory):

    request.cls.kwargs_create_item = kwargs_knowledgebasecategory()

    yield kwargs_knowledgebasecategory

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_knowledgebasecategory):

    yield serializer_knowledgebasecategory
