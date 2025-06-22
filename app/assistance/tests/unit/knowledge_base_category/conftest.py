import pytest



@pytest.fixture( scope = 'class')
def model(model_knowledgebasecategory):

    yield model_knowledgebasecategory


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_knowledgebasecategory):

    request.cls.kwargs_create_item = kwargs_knowledgebasecategory.copy()

    yield kwargs_knowledgebasecategory.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
