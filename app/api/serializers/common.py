
from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import Tenant

from core import fields as centurion_field
from core.lib.feature_not_used import FeatureNotUsed



class OrganizationField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        """ Queryset Override
        
        Override the base serializer and filter out the `global_organization`
        if defined.
        """

        queryset = Tenant.objects.all()

        if self.context.get('request', None):

            if hasattr(self.context['request'], 'app_settings'):

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

        get_url = {
            '_self': item.get_url( request = self._context['view'].request ),
        }

        kb_model_name = self.Meta.model._meta.model_name
        if getattr(item, 'kb_model_name'):

            kb_model_name = item.kb_model_name


        get_url['knowledge_base'] = reverse(
            'v2:_api_v2_model_kb-list',
            request=self._context['view'].request,
            kwargs={
                'model': kb_model_name,
                'model_pk': item.pk
            }
        )

        if getattr(self.Meta.model, 'save_model_history', True):

            history_app_label = self.Meta.model._meta.app_label
            if getattr(item, 'history_app_label'):

                history_app_label = item.history_app_label


            history_model_name = self.Meta.model._meta.model_name
            if getattr(item, 'history_model_name'):

                history_model_name = item.history_model_name


            get_url['history'] = reverse(
                "v2:_api_v2_model_history-list",
                request = self._context['view'].request,
                kwargs = {
                    'app_label': history_app_label,
                    'model_name': history_model_name,
                    'model_id': item.pk
                }
            )


        obj = getattr(item, 'get_url_kwargs_notes', None)

        if callable(obj):

            obj = obj()

        if(
            not str(item._meta.model_name).lower().endswith('notes')
            and obj is not FeatureNotUsed
        ):

            app_namespace = ''

            if getattr(item, 'app_namespace', None):

                app_namespace = str(item.app_namespace) + ':'

            note_basename = app_namespace + '_api_v2_' + str(item._meta.verbose_name).lower().replace(' ', '_') + '_note'

            if getattr(item, 'note_basename'):

                note_basename = app_namespace + item.note_basename

            if getattr(self.Meta, 'note_basename', None):

                note_basename = self.Meta.note_basename

            get_url['notes'] = reverse(
                "v2:" + note_basename + "-list",
                request = self._context['view'].request,
                kwargs = item.get_url_kwargs_notes()
            )

        return get_url
