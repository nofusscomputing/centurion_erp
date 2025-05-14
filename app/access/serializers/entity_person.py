from drf_spectacular.utils import extend_schema_serializer

from access.models.person import Person

from access.serializers.entity import (
    BaseSerializer as BaseBaseSerializer,
    ModelSerializer as BaseModelSerializer,
)
from access.serializers.organization import TenantBaseSerializer



class BaseSerializer(
    BaseBaseSerializer,
):

    pass



@extend_schema_serializer(component_name = 'PersonEntityModelSerializer')
class ModelSerializer(
    BaseSerializer,
    BaseModelSerializer,
):
    """Person Model

    This model inherits from the Entity base model.
    """


    class Meta:

        model = Person

        fields =  [
            'id',
            'entity_ptr_id',
            'organization',
            'entity_type',
            'display_name',
            'f_name',
            'm_name',
            'l_name',
            'dob',
            'model_notes',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'entity_type',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'PersonEntityViewSerializer')
class ViewSerializer(
    ModelSerializer,
):
    """Person View Model

    This model inherits from the Entity base model.
    """

    organization = TenantBaseSerializer(many=False, read_only=True)
