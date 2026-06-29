from core.models.ticket_base import TicketBase



class ProjectTaskTicket(
    TicketBase
):

    _is_submodel = True

    url_model_name = 'project_ticket'


    class Meta:

        ordering = [
            'id',
        ]

        permissions = [
            ('import_projecttaskticket', 'Can import project task ticket'),
            ('purge_projecttaskticket', 'Can purge project task ticket'),
            ('triage_projecttaskticket', 'Can triage project task ticket'),
        ]

        verbose_name = 'Project Task'

        verbose_name_plural = 'Project Tasks'



    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        del kwargs['app_label']

        kwargs.update({
            'project_id': self.project.id,
        })


        return kwargs
