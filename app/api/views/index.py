from django.utils.safestring import mark_safe

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse



class Index(viewsets.ViewSet):

    permission_classes = [
        IsAuthenticated,
    ]


    def get_view_name(self):
        return "API"

    def get_view_description(self, html=False) -> str:
        text = "Centurion ERP Rest API"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    def list(self, request, pk=None):

        API: dict = {
            'v2': reverse("v2:_api_v2_home-list", request=request)
        }

        return Response( API )
