
from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import Organization

from core import fields as centurion_field




class OrganizationField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        """ Queryset Override
        
        Override the base serializer and filter out the `global_organization`
        if defined.
        """

        queryset = Organization.objects.all()

        if self.context.get('request', None):

            if getattr(self.context['request'].app_settings, 'global_organization', None):

                queryset = queryset.exclude(id=self.context['request'].app_settings.global_organization.id)

        return queryset



class CommonBaseSerializer(serializers.ModelSerializer):

    pass



class CommonModelSerializer(CommonBaseSerializer):
    """Common Model Serializer

    _**Note:** This serializer is not inherited by the organization Serializer_
    _`access.serializers.organization`, this is by design_

    This serializer is included within ALL model (Tenancy Model) serilaizers and is intended to be used
    to add objects that ALL model serializers will require.

    Args:
        CommonBaseSerializer (Class): Common base serializer
    """

    model_notes = centurion_field.MarkdownField( required = False )
    
    organization = OrganizationField(required = False)


    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),

            'history': reverse(
                "v2:_api_v2_model_history-list",
                request = self._context['view'].request,
                kwargs = {
                    'app_label': self.Meta.model._meta.app_label,
                    'model_name': self.Meta.model._meta.model_name,
                    'model_id': item.pk
                }
            ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_operating_system_note-list",
                request = self._context['view'].request,
                kwargs = {
                    'model_id': item.pk
                }
            ),
        }
