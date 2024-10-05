from django.utils.safestring import mark_safe

from rest_framework import generics, permissions, routers, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

# from .metadata import NavigationMetadata


class Index(viewsets.ViewSet):

    # metadata_class = NavigationMetadata

    permission_classes = []

    def get_view_name(self):
        return "Assistance"

    def get_view_description(self, html=False) -> str:
        text = "Assistance Module"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def list(self, request, pk=None):
        return Response(
            {
                "requets": reverse('API:_api_v2_ticket_request-list', request=request)
            }
        )
