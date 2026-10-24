import pytest




@pytest.fixture( scope = 'class')
def model(request, model_itassetoperatingsystem):

    request.cls.model = model_itassetoperatingsystem

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from itam.serializers.assetbase_itassetoperatingsystem import ModelSerializer


    yield ModelSerializer


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetoperatingsystem):

    request.cls.kwargs_create_item = kwargs_itassetoperatingsystem()

    yield kwargs_itassetoperatingsystem

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass
