from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.viewsets.common import IndexViewset



@extend_schema(exclude = True)
class Index(IndexViewset):

    allowed_methods: list = [
        'GET',
        'HEAD',
        'OPTIONS'
    ]

    view_description = "Human Resources Module"

    view_name = "Human Resources"


    def list(self, request, pk=None):

        response = {
                "employee": reverse( 'v2:_api_entity_sub-list', request=request, kwargs = { 'entity_model': 'employee' } ),
            }

        return Response(response)
