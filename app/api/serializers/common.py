from django.conf import settings

from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)

from rest_framework import serializers
from rest_framework.exceptions import (
    ValidationError
)
from rest_framework.reverse import reverse

from access.models.tenant import Tenant

from core.mixins.centurion import Centurion
from core import fields as centurion_field



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

    This serializer is included within ALL model (Tenancy Model) serilaizers
    and is intended to be used to add objects that ALL model serializers will
    require.

    Args:
        CommonBaseSerializer (Class): Common base serializer
    """

    model_notes = centurion_field.MarkdownField( required = False )

    organization = OrganizationField(required = False)

    _urls = serializers.SerializerMethodField( method_name = 'get_url_fields' )


    def get_url(self, item) -> dict:
        """Build a models URL dict

        Dynamically build a models URL dict for the API response.

        Args:
            item (CenturionModel): Centurion model to build for.

        Returns:
            dict: URLs dict for model in question
        """

        get_url = {
            '_self': item.get_url(),
        }

        kb_model_name = self.Meta.model._meta.model_name
        if getattr(item, 'kb_model_name', None):

            kb_model_name = item.kb_model_name


        get_url['knowledge_base'] = reverse(
            'v2:_api_v2_model_kb-list',
            request = None,
            kwargs={
                'model': kb_model_name,
                'model_pk': item.pk
            }
        )

        if getattr(self.Meta.model, 'save_model_history', True):

            history_app_label = self.Meta.model._meta.app_label
            if getattr(item, 'history_app_label', None):

                history_app_label = item.history_app_label


            history_model_name = self.Meta.model._meta.model_name
            if getattr(item, 'history_model_name', None):

                history_model_name = item.history_model_name


            if getattr(self.Meta.model, '_audit_enabled', False):

                get_url['history'] = reverse(
                    "v2:_api_centurionaudit_sub-list",
                    request = None,
                    kwargs = {
                        'app_label': history_app_label,
                        'model_name': history_model_name,
                        'model_id': item.pk
                    }
                )

            # elif(
            #     history_app_label is not None
            #     and history_model_name is not None
            #     and not hasattr(self.Meta.model, '_audit_enabled')
            # ):

            #     get_url['history'] = reverse(
            #         "v2:_api_v2_model_history-list",
            #         request = self._context['view'].request,
            #         kwargs = {
            #             'app_label': history_app_label,
            #             'model_name': history_model_name,
            #             'model_id': item.pk
            #         }
            #     )


        obj = getattr(item, 'get_url_kwargs_notes', None)

        if callable(obj):

            obj = obj()

        # if(
        #     not str(item._meta.model_name).lower().endswith('notes')
        #     and obj is not FeatureNotUsed
        #     and not hasattr(self.Meta.model, '_notes_enabled')
        # ):

        #     app_namespace = ''

        #     if getattr(item, 'app_namespace', None):

        #         app_namespace = str(item.app_namespace) + ':'

        #     note_basename = app_namespace + '_api_v2_' + str(item._meta.verbose_name).lower().replace(' ', '_') + '_note'

        #     if getattr(item, 'note_basename', None):

        #         note_basename = app_namespace + item.note_basename

        #     if getattr(self.Meta, 'note_basename', None):

        #         note_basename = self.Meta.note_basename

        #     if getattr(item, 'get_url_kwargs_notes', None):

        #         get_url['notes'] = reverse(
        #             "v2:" + note_basename + "-list",
        #             request = self._context['view'].request,
        #             kwargs = item.get_url_kwargs_notes()
        #         )

        app_label = item._meta.app_label

        model_name = item._meta.model_name

        if item._is_submodel:

            app_label = item._base_model._meta.app_label
            model_name = item._base_model._meta.model_name

        if getattr(self.Meta.model, '_notes_enabled', False):

            get_url['notes'] = reverse(
                "v2:_api_centurionmodelnote_sub-list",
                request = None,
                kwargs = {
                    'app_label': app_label,
                    'model_name': model_name,
                    'model_id': item.pk
                }
            )


        app_label = item._meta.app_label

        model_name = item._meta.model_name

        if item._is_submodel:

            app_label = item._base_model._meta.app_label
            model_name = item._base_model._meta.model_name


        if getattr(item, '_ticket_linkable', False):
            get_url['tickets'] = reverse(
                "v2:_api_modelticket_sub-list",
                request = None,
                kwargs = {
                    'app_label': app_label,
                    'model_name': model_name,
                    'model_id': item.pk
                }
            )


        return get_url


    def get_url_fields(self, item) -> dict:

        url_dict = self.get_url( item = item )

        urls = {}

        if self.context['request'].accepted_media_type == 'text/html':

            return {
                name: f"{settings.SITE_URL}{url}"
                for name, url in url_dict.items()
            }


        return url_dict


    def validate(self, attrs):
        """ Common Serializer Validation

        This function must be called by **all** child serializers. Flow is as follows:

        - Built-in DRF validations.

        - Foreign Key permission check.

        When inheriting this class, this method should be called after any `attr` changes from
        the child serializer. Failing to do so may allow an object to be used that a user does
        not have access to.


        ## Foreign Key permissions check

        Checks every field provided by the user that is a foreign key. On finding a foreign key
        that was supplied by the user as part of a `create` or `update` request. That items tenancy
        along with its view permission is used to check if the user has access to it. If not a
        validation error `HTTP/400` is raised letting the user know that the pk of that item does
        not exist. Even though the object does exist, always return `not found` so the user is
        unable to determine any valid id's of that model.

        """

        validated_attrs = super().validate(attrs)

        if self.context.get('view', None):

            if getattr(self.context['view'], 'action', None) in [
                'create',
                'partial_update',
                'update',
            ]:

                for field_name, value in attrs.items():

                    id = self.initial_data.get(field_name, None)

                    if(
                        field_name in [
                            'organization'
                        ]
                        or not issubclass(value.__class__, Centurion)
                        or id == None
                        or field_name in self.Meta.read_only_fields
                    ):
                        continue


                    model = value.__class__

                    obj = model.objects.get( id = id )

                    if not self.context['request'].user.has_perm(
                        permission = f'{obj._meta.app_label}.view_{obj._meta.model_name}',
                        tenancy = obj.get_organization()
                    ):

                        self.context.get('view').get_log().notice(
                            msg = (
                                f"User {self.context['request'].user.username} tried to "
                                f"access {obj._meta.model_name} with pk={obj.pk}"
                            )
                        )

                        raise ValidationError(
                            detail = {
                                field_name: f"Invalid pk '{id}' - object does not exist."
                            },
                        )    # Dont use `code` kwarg as it leaks via API.


        return validated_attrs



    def is_valid(self, *, raise_exception=False):
        is_valid = False

        try:
            is_valid = super().is_valid(raise_exception=raise_exception)
        except DjangoValidationError as ex:

            if raise_exception:
                raise ValidationError( serializers.as_serializer_error(ex ) )


        return is_valid


    def save(self, **kwargs):
        save = None

        try:

            save = super().save( **kwargs )

        except DjangoValidationError as ex:

                raise ValidationError( serializers.as_serializer_error(ex ) )


        return save
