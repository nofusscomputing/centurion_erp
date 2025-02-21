from django.db import models

from core.models.model_history import ModelHistory

from settings.models.app_settings import AppSettings



class AppSettingsHistory(
    ModelHistory
):


    class Meta:

        db_table = 'settings_appsettings_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'App Settings History'

        verbose_name_plural = 'App Settingsk History'


    model = models.ForeignKey(
        AppSettings,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_object(self):

        return self


    def get_serialized_model(self, serializer_context):

        model = None

        from settings.serializers.app_settings import AppSettingsBaseSerializer

        model = AppSettingsBaseSerializer(self.model, context = serializer_context)

        return model
