import pytest



@pytest.fixture( scope = 'class')
def model(mixin_centurion):

    yield mixin_centurion


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request):

    request.cls.kwargs_create_item = {}

    yield {}
