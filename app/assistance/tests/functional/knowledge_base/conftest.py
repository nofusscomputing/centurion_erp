import pytest



@pytest.fixture( scope = 'class')
def model(model_knowledgebase):

    yield model_knowledgebase


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_knowledgebase):

    request.cls.kwargs_create_item = kwargs_knowledgebase.copy()

    yield kwargs_knowledgebase.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_knowledgebase):

    yield serializer_knowledgebase
