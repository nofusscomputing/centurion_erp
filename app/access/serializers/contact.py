from drf_spectacular.utils import extend_schema_serializer

from access.models.contact import Contact

from access.serializers.person import (
    BaseSerializer as BaseBaseSerializer,
    ModelSerializer as BaseModelSerializer,
)
from access.serializers.organization import OrganizationBaseSerializer



class BaseSerializer(
    BaseBaseSerializer,
):

    pass



@extend_schema_serializer(component_name = 'ContactEntityModelSerializer')
class ModelSerializer(
    BaseSerializer,
    BaseModelSerializer,
):
    """Contact Model

    This model first inherits from Person then inherits from the Entity Base model.
    """


    class Meta:

        model = Contact

        fields = [
            'id',
            'person_ptr_id',
            'organization',
            'entity_type',
            'display_name',
            'f_name',
            'm_name',
            'l_name',
            'dob',
            'email',
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



@extend_schema_serializer(component_name = 'ContactEntityViewSerializer')
class ViewSerializer(
    ModelSerializer,
    ):
    """Contact View Model

    This model inherits from the Person model.
    """

    organization = OrganizationBaseSerializer(many=False, read_only=True)
