from django import forms
from django.db.models import Q

from access.models.tenant import Tenant as Organization
from access.models.team_user import TeamUsers

from core.forms.common import CommonModelForm

from settings.models.app_settings import AppSettings


class AppSettingsForm(CommonModelForm):

    class Meta:

        fields = AppSettings.__all__

        model = AppSettings
