from core.models.ticket_base import TicketBase



class ProjectTaskTicket(
    TicketBase
):

    _is_submodel = True


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_projecttaskticket', 'Can import project task ticket'),
            ('purge_projecttaskticket', 'Can purge project task ticket'),
            ('triage_projecttaskticket', 'Can triage project task ticket'),
        ]

        sub_model_type = 'projecttask'

        verbose_name = 'Project Task'

        verbose_name_plural = 'Project Tasks'
