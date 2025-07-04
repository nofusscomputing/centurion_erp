import pytest



@pytest.fixture( scope = 'class')
def model(model_tenancyabstract):

    yield model_tenancyabstract


@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_tenancyabstract):

    request.cls.kwargs_create_item = kwargs_tenancyabstract.copy()

    yield kwargs_tenancyabstract.copy()

    del request.cls.kwargs_create_item
