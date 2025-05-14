import django
import zoneinfo

from rest_framework.reverse import reverse

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from access.fields import *
from access.models.tenant import Tenant

from core.lib.feature_not_used import FeatureNotUsed

sorted_timezones = sorted(zoneinfo.available_timezones())

TIMEZONES = tuple(zip(
    sorted_timezones,
    sorted_timezones
))

User = django.contrib.auth.get_user_model()



class UserSettingsCommonFields(models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID for this user Setting',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    slug = None

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class UserSettings(UserSettingsCommonFields):

    class Meta:

        ordering = [
            'user'
        ]

        verbose_name = 'User Settings'

        verbose_name_plural = 'User Settings'


    class BrowserMode(models.IntegerChoices):

        AUTO  = 1, 'Auto'
        DARK  = 2, 'Dark'
        LIGHT = 3, 'Light'


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank= False,
        help_text = 'User this Setting belongs to',
        on_delete=models.CASCADE,
        related_name='user_settings',
        verbose_name = 'User'
    )

    browser_mode = models.IntegerField(
        blank = False,
        choices = BrowserMode,
        default = BrowserMode.AUTO,
        help_text = "Set your web browser's mode",
        verbose_name = 'Browser Mode',
    ) 

    default_organization = models.ForeignKey(
        Tenant,
        blank= True,
        default = None,
        help_text = 'Users default Tenant',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Default Tenant'
    )

    timezone = models.CharField(
        default='UTC',
        choices=TIMEZONES,
        help_text = 'What Timezone do you wish to have times displayed in',
        max_length=32,
        verbose_name = 'Your Timezone',
    )

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


    def get_organization(self):

        return self.default_organization



    def get_url( self, request = None ) -> str:

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_user_settings-detail", request=request, kwargs = { 'pk': self.pk } )

        return reverse(f"v2:_api_v2_user_settings-detail", kwargs = { 'pk': self.pk } )


    def get_url_kwargs_notes(self):

        return FeatureNotUsed



    @receiver(post_save, sender=User)
    def new_user_callback(sender, **kwargs):
        settings = UserSettings.objects.filter(user=kwargs['instance'])

        if not settings.exists():

            UserSettings.objects.create(user=kwargs['instance'])

            # settings = UserSettings.objects.filter(user=context.user)


    def is_owner(self, user: int) -> bool:

        if user == self.user:

            return True

        return False
