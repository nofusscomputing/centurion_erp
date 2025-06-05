import pytest

from access.models.tenancy_abstract import TenancyAbstractModel

@pytest.fixture( scope = 'class')
def model_tenancyabstract():

    def clean_model():
        the_model = TenancyAbstractModel

        the_model.context = {
            'logger': None,
            'user': None,
        }

        return the_model

    yield clean_model()



@pytest.fixture( scope = 'class')
def kwargs_tenancyabstract(organization_one):

    kwargs = {
        'organization': organization_one
    }

    yield kwargs.copy()
