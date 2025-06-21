from drf_spectacular.utils import extend_schema_serializer

from access.serializers.entity_contact import (
    BaseSerializer as ContactBaseSerializer,
    ModelSerializer as ContactModelSerializer,
)
from access.serializers.organization import TenantBaseSerializer

from human_resources.models.employee import Employee



class BaseSerializer(
    ContactBaseSerializer,
):

    pass



@extend_schema_serializer(component_name = 'EmployeeEntityModelSerializer')
class ModelSerializer(
    BaseSerializer,
    ContactModelSerializer,
):
    """Employee Model

    This model inherits from Contact model.
    """


    class Meta:

        model = Employee

        fields = [
            'id',
            'person_ptr_id',
            'organization',
            'entity_type',
            'display_name',
            'employee_number',
            'f_name',
            'm_name',
            'l_name',
            'dob',
            'email',
            'directory',
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



@extend_schema_serializer(component_name = 'EmployeeEntityViewSerializer')
class ViewSerializer(
    ModelSerializer,
    ):
    """Employee View Model

    This model inherits from the Contact model.
    """

    organization = TenantBaseSerializer(many=False, read_only=True)
