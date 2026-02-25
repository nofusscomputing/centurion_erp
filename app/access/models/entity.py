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

        verbose_name = 'Entity'

        verbose_name_plural = 'Entities'


    modified = AutoLastModifiedField()



    def __str__(self) -> str:

        related_model = self.get_related_model()

        if related_model is not self:
            return str( related_model )
        
        return f'{self._meta.verbose_name} {self.pk}'
 


    page_layout: dict = []

    table_fields: list = [
        'organization',
        'display_name',
        'created',
        'modified',
    ]
