from django.db import models

from core.models.model_history import ModelHistory

from itim.models.clusters import Cluster



class ClusterHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itim_cluster_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Cluster History'

        verbose_name_plural = 'Cluster History'


    model = models.ForeignKey(
        Cluster,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_object(self):

        return self


    def get_serialized_model(self, serializer_context):

        model = None

        from itim.serializers.cluster import ClusterBaseSerializer

        model = ClusterBaseSerializer(self.model, context = serializer_context)

        return model
