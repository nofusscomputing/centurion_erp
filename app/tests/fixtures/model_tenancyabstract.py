import pytest

from access.models.tenancy_abstract import TenancyAbstractModel

@pytest.fixture( scope = 'class')
def model_tenancyabstract():

    the_model = TenancyAbstractModel

    the_model.context = {
        'logger': None,
        'user': None,
    }

    yield the_model

    the_model.context = {
        'logger': None,
        'user': None,
    }



@pytest.fixture( scope = 'class')
def kwargs_tenancyabstract(organization_one):

    kwargs = {
        'organization': organization_one
    }

    yield kwargs.copy()
