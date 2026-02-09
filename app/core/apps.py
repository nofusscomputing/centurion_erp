from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):

        import core.models.meta
        from core.signal import (
            audit_history,
            ticket_action_comment,
            migration_remove_permissions,
        )
