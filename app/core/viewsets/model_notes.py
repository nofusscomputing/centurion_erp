from django.contrib.auth.models import ContentType

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from api.viewsets.common import ModelViewSet

from config_management.models.groups import ConfigGroups

from itam.models.device import Device
from itam.models.operating_system import OperatingSystem
from itam.models.software import Software

from itim.models.services import Service



class ModelNoteViewSet(ModelViewSet):
    """Base class for Model Notes

    This class is intended not to be used directly. It should be used as an
    inherited class.

    The inherited class must include the following class objects:

    - get_serializer_class function

    - model attribute containing the notes model for the model to receive notes
    """

    filterset_fields = []

    parent_model_pk_kwarg = 'model_id'

    search_fields = [
        'content',
    ]


    view_description = 'Model notes'


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = self.model.objects.filter(
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower()
            ).id,
            model = int(self.kwargs['model_id'])
        )

        return self.queryset


    def get_parent_model(self):

        if self.parent_model is None:

            self.parent_model = self.model.model.field.related_model

        return self.parent_model
