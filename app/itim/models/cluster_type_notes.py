from access.fields import *

from core.models.model_notes import ModelNotes

from itim.models.clusters import ClusterType



class ClusterTypeNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itim_cluster_type_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Cluster Type Note'

        verbose_name_plural = 'Cluster Type Notes'


    model = models.ForeignKey(
        ClusterType,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
