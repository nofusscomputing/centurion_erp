from drf_spectacular.utils import extend_schema_serializer

from access.models.company_base import Company

from access.serializers.entity import (
    BaseSerializer as BaseBaseSerializer,
    ModelSerializer as BaseModelSerializer,
)
from access.serializers.organization import TenantBaseSerializer



class BaseSerializer(
    BaseBaseSerializer,
):

    pass



@extend_schema_serializer(component_name = 'CompanyEntityModelSerializer')
class ModelSerializer(
    BaseSerializer,
    BaseModelSerializer,
):
    """Company Model

    This model inherits from the Entity base model.
    """


    class Meta:

        model = Company

        fields =  [
            'id',
            'entity_ptr_id',
            'organization',
            'entity_type',
            'display_name',
            'name',
            'model_notes',
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



@extend_schema_serializer(component_name = 'CompanyEntityViewSerializer')
class ViewSerializer(
    ModelSerializer,
):
    """Company View Model

    This model inherits from the Entity base model.
    """

    organization = TenantBaseSerializer(many=False, read_only=True)
