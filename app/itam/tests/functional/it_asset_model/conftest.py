import pytest

from itam.models import ITAsset



@pytest.fixture( scope = 'class')
def model(model_itassetmodel):


    yield model_itassetmodel



# @pytest.fixture(scope='function')
# def create_serializer():

#     from itam.serializers.assetbase_itasset import ModelSerializer


#     yield ModelSerializer


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetmodel):

    yield kwargs_itassetmodel



@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetmodel):

    yield serializer_itassetmodel
