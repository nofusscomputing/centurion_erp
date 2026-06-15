from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):

        import core.models.meta

        from core.signal import (
            audit_history,
            migration_remove_permissions,
            ticket_action_comment,
            ticket_action_comment_ticket_dependency,
        )
        from core.signal.ticketbase_validation_m2m_assigned_to import (
            ticketbase_validation_m2m_assigned_to
        )
