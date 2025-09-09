import pytest
import logging

from access.viewsets.entity import (
    NoDocsViewSet,
    ViewSet,
)

from api.tests.functional.viewset.test_functional_tenancy_viewset import SubModelViewSetInheritedCases


@pytest.mark.model_entity
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet



class EntityViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class EntityViewsetPyTest(
    ViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
