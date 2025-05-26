import pytest

from centurion.tests.functional_models import ModelTestCases



@pytest.mark.tenancy_models
class TenancyAbstractModelTestCases(
    ModelTestCases
):



    kwargs_create_item = {
        'organization': 'set by fixture - setup_organization'
    }


    @pytest.fixture( scope = 'class', autouse = True)
    def setup_organization(cls, request, model, organization_one):

        request.cls.organization = organization_one
        
        if request.cls.kwargs_create_item:

            request.cls.kwargs_create_item.update({
                'organization': organization_one,
            })

        else:

            request.cls.kwargs_create_item = {
                'organization': organization_one,
            }



class TenancyAbstractModelInheritedCases(
    TenancyAbstractModelTestCases,
):

    pass



class TenancyAbstractModelPyTest(
    TenancyAbstractModelTestCases,
):

    pass
