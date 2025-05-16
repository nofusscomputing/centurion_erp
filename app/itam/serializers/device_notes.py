from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.device_notes import (
    DeviceNotes
)
from itam.serializers.device import DeviceBaseSerializer



class DeviceNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class DeviceNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = DeviceNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class DeviceNoteViewSerializer(
    ModelNoteViewSerializer,
    DeviceNoteModelSerializer,
):

    pass