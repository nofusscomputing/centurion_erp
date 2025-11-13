from django.apps import AppConfig


class ProjectManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_management'

    def ready(self):
        from project_management.models.ticket_project_task import ProjectTaskTicket    # pylint: disable=W0611:unused-import
        return super().ready()
