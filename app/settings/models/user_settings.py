import zoneinfo

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from access.fields import AutoLastModifiedField
from access.managers.user import UserManager
from access.models.tenant import Tenant

from core.models.centurion import CenturionModel

sorted_timezones = sorted(zoneinfo.available_timezones())

TIMEZONES = tuple(zip(
    sorted_timezones,
    sorted_timezones
))



class UserSettings(
    CenturionModel,
):

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    objects = UserManager()


    class Meta:

        ordering = [
            'user'
        ]

        verbose_name = 'User Settings'

        verbose_name_plural = 'User Settings'


    model_notes = False

    organization = None

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'User this Setting belongs to',
        on_delete = models.CASCADE,
        related_name='user_settings',
        verbose_name = 'User'
    )

    class BrowserMode(models.IntegerChoices):

        AUTO  = 1, 'Auto'
        DARK  = 2, 'Dark'
        LIGHT = 3, 'Light'

    browser_mode = models.IntegerField(
        blank = False,
        choices = BrowserMode,
        default = BrowserMode.AUTO,
        help_text = "Set your web browser's mode",
        verbose_name = 'Browser Mode',
    )

    default_organization = models.ForeignKey(
        Tenant,
        blank = True,
        help_text = 'Users default Tenant',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Default Tenant'
    )

    timezone = models.CharField(
        default = 'UTC',
        choices = TIMEZONES,
        help_text = 'What Timezone do you wish to have times displayed in',
        max_length = 32,
        verbose_name = 'Your Timezone',
    )

    modified = AutoLastModifiedField()

    page_layout: list = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        'browser_mode',
                        'default_organization',
                        'timezone',
                    ],
                },
                {
                    "name": "Auth Tokens",
                    "layout": "table",
                    "field": "tokens",
                }
            ]
        },
    ]

    table_fields = []


    def is_owner(self, user: int) -> bool:

        if user == self.user:

            return True

        return False


    def get_organization(self):

        return self.default_organization



    def get_url(
        self, relative: bool = False, api_version: int = 2, many = False, request: any = None
    ) -> str:

        return super().get_url( relative = relative, api_version = api_version, many = False, request = request)



    def get_url_kwargs(self, many = False) -> dict:

        kwargs = {
            'user_id': self.user.id
        }

        return kwargs


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def new_user_callback(sender, **kwargs):

        settings = UserSettings.objects.user(
            user = kwargs['instance'],
            permission = None
        ).filter(user=kwargs['instance'])

        if not settings.exists():

            UserSettings.objects.create(user=kwargs['instance'])

            # settings = UserSettings.objects.filter(user=context.user)
