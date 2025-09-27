import pytest



@pytest.fixture( scope = 'class')
def model(model_modelticketmetamodel):

    yield model_modelticketmetamodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_modelticketmetamodel):

    request.cls.kwargs_create_item = kwargs_modelticketmetamodel.copy()

    yield kwargs_modelticketmetamodel.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_modelticketmetamodel):

    yield serializer_modelticketmetamodel
