from itim.models.slm_ticket_base import SLMTicket



class ChangeTicket(
    SLMTicket
):

    _is_submodel = True


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_changeticket', 'Can import change ticket'),
            ('purge_changeticket', 'Can purge change ticket'),
            ('triage_changeticket', 'Can triage change ticket'),
        ]

        sub_model_type = 'change'

        verbose_name = 'Change'

        verbose_name_plural = 'Changes'

# analysis
#    impacts         - Risk assessment
#    control list    - Risk controls

# planning
#    Deployment plan - 
#    backup          - backup / rollout plan
#    checklist       - Implementation plan

