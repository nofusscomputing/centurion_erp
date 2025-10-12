from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class Entity(
    CenturionModel
):

    @property
    def _base_model(self):

        return Entity

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
