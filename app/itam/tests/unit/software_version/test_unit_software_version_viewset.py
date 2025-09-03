import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.viewsets.software_version import (
    Software,
    SoftwareVersion,
    ViewSet,
)



@pytest.mark.model_softwareversion
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
                    'software'
                ]
            },
            'model': {
                'value': SoftwareVersion
            },
            'model_documentation': {
                'type': type(None),
            },
            'parent_model': {
                'value': Software
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'software_id'
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
                'value': 'Physical Softwares'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



    def test_view_func_get_queryset_cache_result(self, viewset_mock_request):
        """Viewset Test

        Ensure that the `get_queryset` function caches the result under
        attribute `<viewset>.queryset`
        """

        view_set = viewset_mock_request

        view_set.kwargs = {
            'software_id': self.kwargs_create_item['software'].id
        }

        assert view_set.queryset is None    # Must be empty before init

        q = view_set.get_queryset()

        assert view_set.queryset is not None    # Must not be empty after init

        assert q == view_set.queryset



class SoftwareVersionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareVersionViewsetPyTest(
    ViewsetTestCases,
):

    pass
