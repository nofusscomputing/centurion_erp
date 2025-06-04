import pytest

from importlib import reload

from access.models import tenancy_abstract


@pytest.fixture( scope = 'class')
def model_tenancyabstract():

    yield reload(tenancy_abstract).TenancyAbstractModel


@pytest.fixture( scope = 'class')
def kwargs_tenancyabstract(organization_one):

    kwargs = {
        'organization': organization_one
    }

    yield kwargs.copy()
