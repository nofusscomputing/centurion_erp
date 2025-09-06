import pytest

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.tests.unit.test_unit_common_viewset import (
    CommonReadOnlyListModelViewSetInheritedCases
)
from api.viewsets.common.public import (
    JSONAPIMetadata,
    PublicReadOnlyViewSet,
    StaticPageNumbering
)



@pytest.mark.permissions_public_user
@pytest.mark.permissions
class PublicReadOnlyViewSetTestCases(
    CommonReadOnlyListModelViewSetInheritedCases
):

    @property
    def parameterized_class_attributes(self):
        return {
            'pagination_class': {
                'type': type,
                'value': StaticPageNumbering
            },
            'permission_classes': {
                'type': list,
                'value': [
                    IsAuthenticatedOrReadOnly,
                ]
            },
            'metadata_class': {
                'type': type,
                'value': JSONAPIMetadata
            }
        }


class PublicReadOnlyViewSetInheritedCases(
    PublicReadOnlyViewSetTestCases
):
    pass

class PublicUserPermissionsReadOnlyViewSetPyTest(
    PublicReadOnlyViewSetTestCases
):
    @pytest.fixture
    def viewset(self):
        yield PublicReadOnlyViewSet

    @property
    def parameterized_class_attributes(self):
        return {
            '_log': {
                'type': type(None),
                'value': None
            },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'model': {
                'type': type(None),
                'value': None
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'view_description': {
                'type': type(None),
                'value': None
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }

    def test_view_func_get_queryset_cache_result(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_view_func_get_queryset_cache_result_used(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_calls_user(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_pk(self):
        pytest.xfail( reason = 'base class is abstract with no model' )

    def test_function_get_queryset_manager_filters_by_model_id(self):
        pytest.xfail( reason = 'base class is abstract with no model' )
