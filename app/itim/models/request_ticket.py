from itim.models.slm_ticket_base import SLMTicket



class RequestTicket(
    SLMTicket
):

    _is_submodel = True


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_requestticket', 'Can import request ticket'),
            ('purge_requestticket', 'Can purge request ticket'),
            ('triage_requestticket', 'Can triage request ticket'),
        ]

        sub_model_type = 'request'

        verbose_name = 'Request'

        verbose_name_plural = 'Requests'
