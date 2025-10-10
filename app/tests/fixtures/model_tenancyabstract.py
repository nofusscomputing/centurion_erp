import pytest

from access.models.tenancy_abstract import TenancyAbstractModel

@pytest.fixture( scope = 'class')
def model_tenancyabstract():

    the_model = TenancyAbstractModel

    yield the_model



@pytest.fixture( scope = 'class')
def kwargs_tenancyabstract(organization_one):

    def factory():

        kwargs = {
            'organization': organization_one
        }

        return kwargs

    yield factory
