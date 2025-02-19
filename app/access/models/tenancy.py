# from django.conf import settings
from django.db import models
# from django.contrib.auth.models import User, Group

from rest_framework.reverse import reverse

# from .fields import *

from access.models.organization import Organization

from core import exceptions as centurion_exceptions
from core.middleware.get_request import get_request
from core.mixin.history_save import SaveHistory



class TenancyManager(models.Manager):
    """Multi-Tennant Object Manager

    This manager specifically caters for the multi-tenancy features of Centurion ERP.
    """


    def get_queryset(self):
        """ Fetch the data

        This function filters the data fetched from the database to that which is from the organizations
        the user is a part of.

        !!! danger "Requirement"
            This method may be overridden however must still be called from the overriding function. i.e. `super().get_queryset()`

        ## Workflow

        This functions workflow is as follows:

        - Fetch the user from the request

        - Check if the user is authenticated

        - Iterate over the users teams

        - Store unique organizations from users teams

        - return results

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        request = get_request()

        user_organizations: list(str()) = []


        if request:

            if request.app_settings.global_organization:

                user_organizations += [ request.app_settings.global_organization.id ]


            user = request.user


            if user.is_authenticated:

                for team in request.tenancy._user_teams:


                    if team.organization.id not in user_organizations:

                        if not user_organizations:

                            self.user_organizations = []

                        user_organizations += [ team.organization.id ]


                # if len(user_organizations) > 0 and not user.is_superuser and self.model.is_global is not None:
                if len(user_organizations) > 0 and not user.is_superuser:

                    if getattr(self.model, 'is_global', False) is True:

                        return super().get_queryset().filter(
                            models.Q(organization__in=user_organizations)
                            |
                            models.Q(is_global = True)
                        )

                    else:

                        return super().get_queryset().filter(
                            models.Q(organization__in=user_organizations)
                        )

        return super().get_queryset()



class TenancyObject(SaveHistory):
    """ Tenancy Model Abstrct class.

    This class is for inclusion wihtin **every** model within Centurion ERP.
    Provides the required fields, functions and methods for multi tennant objects.
    Unless otherwise stated, **no** object within this class may be overridden.

    Raises:
        ValidationError: User failed to supply organization
    """

    objects = TenancyManager()
    """ Multi-Tenanant Objects """

    class Meta:
        abstract = True


    def validatate_organization_exists(self):
        """Ensure that the user did provide an organization

        Raises:
            ValidationError: User failed to supply organization.
        """

        if not self:
            raise centurion_exceptions.ValidationError('You must provide an organization')


    id = models.AutoField(
        blank=False,
        help_text = 'ID of the item',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    organization = models.ForeignKey(
        Organization,
        blank = False,
        help_text = 'Organization this belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = '+',
        validators = [validatate_organization_exists],
        verbose_name = 'Organization'
    )

    is_global = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this a global object?',
        verbose_name = 'Global Object'
    )

    model_notes = models.TextField(
        blank = True,
        default = None,
        help_text = 'Tid bits of information',
        null = True,
        verbose_name = 'Notes',
    )

    def get_organization(self) -> Organization:
        return self.organization


    def get_url( self, request = None ) -> str:
        """Fetch the models URL

        If URL kwargs are required to generate the URL, define a `get_url_kwargs` that returns them.

        Args:
            request (object, optional): The request object that was made by the end user. Defaults to None.

        Returns:
            str: Canonical URL of the model if the `request` object was provided. Otherwise the relative URL. 
        """

        model_name = str(self._meta.verbose_name.lower()).replace(' ', '_')


        if request:

            return reverse(f"v2:_api_v2_{model_name}-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_{model_name}-detail", kwargs = self.get_url_kwargs() )


    def get_url_kwargs(self) -> dict:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        return {
            'pk': self.id
        }


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.clean()

        if not getattr(self, 'organization', None):

            raise centurion_exceptions.ValidationError(
                detail = {
                    'organization': 'Organization is required'
                },
                code = 'required'
            )

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
