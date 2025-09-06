from rest_framework import pagination

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_json_api.metadata import JSONAPIMetadata

from .tenancy import CommonReadOnlyListModelViewSet



class StaticPageNumbering(
    pagination.PageNumberPagination
):
    """Enforce Page Numbering

    Enfore results per page min/max to static value that cant be changed.
    """

    page_size = 20

    max_page_size = 20



class PublicReadOnlyViewSet(
    CommonReadOnlyListModelViewSet
):
    """Public Viewable ViewSet

    User does not need to be authenticated. This viewset is intended to be
    inherited by viewsets that are intended to be consumed by unauthenticated
    public users.

    URL **must** be prefixed with `public`

    Args:
        ReadOnlyModelViewSet (ViewSet): Common Read-Only Viewset
    """

    pagination_class = StaticPageNumbering

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    metadata_class = JSONAPIMetadata
