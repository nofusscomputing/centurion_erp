import zoneinfo

from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from access.fields import *
from access.models import Organization

sorted_timezones = sorted(zoneinfo.available_timezones())

TIMEZONES = tuple(zip(
    sorted_timezones,
    sorted_timezones
))



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
        User,
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
        Organization,
        blank= True,
        default = None,
        help_text = 'Users default Organization',
        null = True,
        on_delete=models.SET_DEFAULT,
        verbose_name = 'Default Organization'
    )

    timezone = models.CharField(
        default='UTC',
        choices=TIMEZONES,
        help_text = 'What Timezone do you wish to have times displayed in',
        max_length=32,
        verbose_name = 'Your Timezone',
    )


    def get_organization(self):

        return self.default_organization



    def get_url( self, request = None ) -> str:

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_user_settings-detail", request=request, kwargs = { 'pk': self.pk } )

        return reverse(f"v2:_api_v2_user_settings-detail", kwargs = { 'pk': self.pk } )



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
