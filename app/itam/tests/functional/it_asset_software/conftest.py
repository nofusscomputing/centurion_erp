import pytest




@pytest.fixture( scope = 'class')
def model(request, model_itassetsoftware):

    request.cls.model = model_itassetsoftware

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from itam.serializers.assetbase_itassetsoftware import ModelSerializer


    yield ModelSerializer


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetsoftware):

    request.cls.kwargs_create_item = kwargs_itassetsoftware()

    yield kwargs_itassetsoftware

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass
