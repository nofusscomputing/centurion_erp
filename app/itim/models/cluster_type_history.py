from django.db import models

from core.models.model_history import ModelHistory

from itim.models.clusters import ClusterType



class ClusterTypeHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itim_clustertype_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Cluster Type History'

        verbose_name_plural = 'Cluster Type History'


    model = models.ForeignKey(
        ClusterType,
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

        from itim.serializers.cluster_type import ClusterTypeBaseSerializer

        model = ClusterTypeBaseSerializer(self.model, context = serializer_context)

        return model
