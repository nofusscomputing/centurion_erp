from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class Entity(
    CenturionModel
):

    model_tag = 'entity'

    documentation = ''

    kb_model_name = 'entity'

    url_model_name = 'entity'


    class Meta:

        ordering = [
            'created',
            'modified',
            'organization',
        ]

        sub_model_type = 'entity'

        verbose_name = 'Entity'

        verbose_name_plural = 'Entities'


    entity_type = models.CharField(
        blank = False,
        help_text = 'Type this entity is',
        max_length = 30,
        unique = False,
        verbose_name = 'Entity Type'
    )

    modified = AutoLastModifiedField()



    def __str__(self) -> str:

        related_model = self.get_related_model()

        if related_model is None:

            return f'{self.entity_type} {self.pk}'


        return str( related_model )


    page_layout: dict = []

    table_fields: list = [
        'organization',
        'entity_type',
        'display_name',
        'created',
        'modified',
    ]



    def clean_fields(self, exclude = None ):

        related_model = self.get_related_model()

        if related_model is None:

            related_model = self

        if self.entity_type != str(related_model._meta.verbose_name).lower().replace(' ', '_'):

            self.entity_type = str(related_model._meta.verbose_name).lower().replace(' ', '_')

        super().clean_fields( exclude = exclude )



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


    def get_url_kwargs(self, many = False) -> dict:

        model = self.get_related_model()

        if (len(self._meta.parents) == 0 and model is None) or not many:

            return {
                'pk': self.id
            }

        if model is None:

            model = self

        kwargs = {
            'entity_model': str(model._meta.verbose_name).lower().replace(' ', '_'),
        }

        return kwargs
