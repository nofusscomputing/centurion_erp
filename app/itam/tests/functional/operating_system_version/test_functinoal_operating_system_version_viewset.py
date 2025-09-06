import pytest

from django.db import models

from api.tests.functional.viewset.test_functional_tenancy_viewset import ModelViewSetInheritedCases

from itam.viewsets.operating_system_version import (
    ViewSet,
)



@pytest.mark.model_operatingsystemversion
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class OperatingSystemVersionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemVersionViewsetPyTest(
    ViewsetTestCases,
):

    pass
