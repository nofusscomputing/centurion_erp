from django.db import models

from core.models.ticket_base import TicketBase



class SLMTicket(
    TicketBase
):
    """Ticket Type

    Base Ticket Type for tickets that require Servie Level Management.
    """

    _is_submodel = True


    class Meta:

        ordering = [
            'id',
        ]

        verbose_name = 'SLM Ticket Base'

        verbose_name_plural = 'SLM Tickets'



    # SLA = models.ForeignKey(
    #     ServiceLevelAgreement,
    #     blank = True,
    #     help_text = 'Service Level Agreement this ticket is covered under',
    #     null = True,
    #     on_delete = models.PROTECT,
    #     verbose_name = 'SLA',
    # )

    ttr = models.IntegerField(
        blank = True,
        default = 0,
        help_text = 'Time taken to resolve the ticket / Time to Resolution (TTR)',
        null = False,
        verbose_name = 'TTR',
    )    # Set when ticket is closed and always update to the latest close date

    tto = models.IntegerField(
        blank = True,
        default = 0,
        help_text = 'Time taken to Acknowledge ticket / Time to Ownership (TTO)',
        null = False,
        verbose_name = 'TTO',
    )    # set to the time when the ticket is first assigned. DONT update ever.
