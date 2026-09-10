from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from api.serializers import common

from centurion.models.meta import FeatureFlagAuditHistory # pylint: disable=E0401:import-error disable=E0611:no-name-in-module

from core.serializers.centurionaudit import (
    BaseSerializer,
    ViewSerializer as AuditHistoryViewSerializer
)




@extend_schema_serializer(component_name = 'FeatureFlagAuditHistoryModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Git Group Audit History Base Model"""


    class Meta:

        model = FeatureFlagAuditHistory

        fields = [
            'id',
            'organization',
            'display_name',
            'content_type',
            'model',
            'before',
            'after',
            'action',
            'user',
            'created',
            '_urls',
        ]

        read_only_fields = fields



@extend_schema_serializer(component_name = 'FeatureFlagAuditHistoryViewSerializer')
class ViewSerializer(
    ModelSerializer,
    AuditHistoryViewSerializer,
):
    """Git Group Audit History Base View Model"""
    pass
