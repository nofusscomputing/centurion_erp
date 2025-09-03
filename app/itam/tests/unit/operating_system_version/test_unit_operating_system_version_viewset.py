import pytest

from django.db import models

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.viewsets.operating_system_version import (
    OperatingSystem,
    OperatingSystemVersion,
    ViewSet,
)



@pytest.mark.model_operatingsystemversion
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'organization',
                ]
            },
            'model': {
                'value': OperatingSystemVersion
            },
            'model_documentation': {
                'type': type(None),
            },
            'parent_model': {
                'type': models.base.ModelBase,
                'value': OperatingSystem
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'operating_system_id'
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name'
                ]
            },
            'view_description': {
                'value': 'Operating Systems'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }


    def test_view_func_get_queryset_cache_result(self, viewset_mock_request,
        # kwargs_create_item
    ):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        view_set.kwargs = {
            'operating_system_id': self.kwargs_create_item['operating_system'].id
        }

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset



class OperatingSystemVersionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemVersionViewsetPyTest(
    ViewsetTestCases,
):

    pass
