from django.db import models

from itim.models.slm_ticket_base import SLMTicket



class ProblemTicket(
    SLMTicket
):

    _is_submodel = True


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_problemticket', 'Can import problem ticket'),
            ('purge_problemticket', 'Can purge problem ticket'),
            ('triage_problemticket', 'Can triage problem ticket'),
        ]

        sub_model_type = 'problem'

        verbose_name = 'Problem'

        verbose_name_plural = 'Problems'



    business_impact = models.TextField(
        blank = True,
        help_text = 'Description of the impact to operations.',
        null = True,
        verbose_name = 'Business Impact',
    ) # text, markdown



    cause_analysis = models.TextField(
        blank = True,
        help_text = 'Detailed technical analysis identifying root cause.',
        null = True,
        verbose_name = 'Root Cause Analysis (RCA)',
    ) # text, markdown



    observations = models.TextField(
        blank = True,
        help_text = 'Summary of known symptoms or evidence.',
        null = True,
        verbose_name = 'Observation(s)',
    ) # text, markdown



    workaround = models.TextField(
        blank = True,
        help_text = 'Temporary fix allowing service continuation.',
        null = True,
        verbose_name = 'Workaround(s)',
    ) # text, markdown
