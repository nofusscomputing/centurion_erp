import pytest



@pytest.fixture( scope = 'class')
def model(model_tenant):

    yield model_tenant


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_tenant):

    request.cls.kwargs_create_item = kwargs_tenant()

    yield kwargs_tenant

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_tenant):

    yield serializer_tenant
