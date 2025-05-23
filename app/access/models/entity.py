from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject

from core.lib.feature_not_used import FeatureNotUsed



class Entity(
    TenancyObject
):


    class Meta:

        ordering = [
            'created',
            'modified',
            'organization',
        ]

        sub_model_type = 'entity'

        verbose_name = 'Entity'

        verbose_name_plural = 'Entities'


    id = models.AutoField(
        blank=False,
        help_text = 'Primary key of the entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    entity_type = models.CharField(
        blank = False,
        help_text = 'Type this entity is',
        max_length = 30,
        unique = False,
        verbose_name = 'Entity Type'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



    def __str__(self) -> str:
        
        related_model = self.get_related_model()

        if related_model is None:

            return f'{self.entity_type} {self.pk}'


        return str( related_model )



    # app_namespace = 'access'

    history_app_label = 'access'

    history_model_name = 'entity'

    kb_model_name = 'entity'

    note_basename = '_api_v2_entity_note'

    documentation = ''

    page_layout: dict = []


    table_fields: list = [
        'organization',
        'entity_type',
        'display_name',
        'created',
        'modified',
    ]


    def get_related_field_name(self) -> str:

        meta = getattr(self, '_meta')

        for related_object in getattr(meta, 'related_objects', []):

            if not issubclass(related_object.related_model, Entity):

                continue

            if getattr(self, related_object.name, None):

                if( 
                    not str(related_object.name).endswith('history')
                    and not str(related_object.name).endswith('notes')
                ):

                    return related_object.name
                    break


        return ''


    def get_related_model(self):
        """Recursive model Fetch

        Returns the lowest model found in a chain of inherited models.

        Args:
            model (models.Model, optional): Model to fetch the child model from. Defaults to None.

        Returns:
            models.Model: Lowset model found in inherited model chain
        """

        related_model_name = self.get_related_field_name()

        related_model = getattr(self, related_model_name, None)

        if related_model_name == '':

            related_model = None

        elif related_model is None:

            related_model = self

        elif hasattr(related_model, 'get_related_field_name'):

            if related_model.get_related_field_name() != '':

                related_model = related_model.get_related_model()


        return related_model


    def get_url_kwargs(self) -> dict:

        model = self.get_related_model()

        if len(self._meta.parents) == 0 and model is None:

            return {
                'pk': self.id
            }

        if model is None:

            model = self

        kwargs = {
            'entity_model': str(model._meta.verbose_name).lower().replace(' ', '_'),
        }

        if model.pk:

            kwargs.update({
                'pk': model.id
            })

        return kwargs



    def get_url( self, request = None ) -> str:
        """Fetch the models URL

        If URL kwargs are required to generate the URL, define a `get_url_kwargs` that returns them.

        Args:
            request (object, optional): The request object that was made by the end user. Defaults to None.

        Returns:
            str: Canonical URL of the model if the `request` object was provided. Otherwise the relative URL. 
        """

        model = None

        if getattr(self, 'get_related_model', None):

            model = self.get_related_model()


        
        if model is None:

            model = self


        sub_entity = ''
        if model._meta.model_name != 'entity':

            sub_entity = '_sub'


        kwargs = self.get_url_kwargs()

        view = 'list'
        if 'pk' in kwargs:

            view = 'detail'

        if request:

            return reverse(f"v2:" + model.get_app_namespace() + f"_api_v2_entity" + sub_entity + "-" + view, request=request, kwargs = kwargs )

        return reverse(f"v2:" + model.get_app_namespace() + f"_api_v2_entity" + sub_entity + "-" + view, kwargs = kwargs )



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        related_model = self.get_related_model()

        if related_model is None:

            related_model = self

        if self.entity_type != str(related_model._meta.verbose_name).lower().replace(' ', '_'):

            self.entity_type = str(related_model._meta.verbose_name).lower().replace(' ', '_')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    def save_history(self, before: dict, after: dict) -> bool:

        from access.models.entity_history import EntityHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = EntityHistory
        )

        return history
