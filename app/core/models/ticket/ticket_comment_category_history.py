from django.db import models

from core.models.model_history import ModelHistory

from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentCategoryHistory(
    ModelHistory
):


    class Meta:

        db_table = 'core_ticketcommentcategory_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Ticket Comment Category History'

        verbose_name_plural = 'Ticket Comment Category History'


    model = models.ForeignKey(
        TicketCommentCategory,
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

        from core.serializers.ticket_comment_category import TicketCommentCategoryBaseSerializer

        model = TicketCommentCategoryBaseSerializer(self.model, context = serializer_context)

        return model
