from itim.models.slm_ticket_base import SLMTicket



class IncidentTicket(
    SLMTicket
):


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_incidentticket', 'Can import incident ticket'),
            ('purge_incidentticket', 'Can purge incident ticket'),
            ('triage_incidentticket', 'Can triage incident ticket'),
        ]

        sub_model_type = 'incident'

        verbose_name = 'Incident'

        verbose_name_plural = 'Incidents'
