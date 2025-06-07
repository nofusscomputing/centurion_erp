import pytest




@pytest.fixture( scope = 'class')
def model(model_featureflag):

    yield model_featureflag


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_featureflag):

    request.cls.kwargs_create_item = kwargs_featureflag.copy()

    yield kwargs_featureflag.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
