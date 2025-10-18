from django.core.exceptions import (
    ValidationError,
)
from django.db import models

from access.managers.tenancy import TenancyManager
from access.models.tenant import Tenant



class TenancyAbstractModel(
    models.Model,
):
    """ Tenancy Model Abstract class.

    This class is for inclusion within **every** model within Centurion ERP.
    Provides the required fields, functions and methods for multi tennant objects.
    Unless otherwise stated, **no** object within this class may be overridden.

    Raises:
        ValidationError: User failed to supply organization
    """

    objects = TenancyManager()
    """ ~~Multi-Tenant Manager~~

    **Note:** ~~This manager relies upon the model class having `context['user']`
    set. without a user the manager can not perform multi-tenant queries.~~
    """


    class Meta:
        abstract = True


    def validatate_organization_exists(self):
        """Ensure that the user did provide an organization

        Raises:
            ValidationError: User failed to supply organization.
        """

        if not self:
            raise ValidationError(
                code = 'required',
                message = 'You must provide an organization'
            )

    organization = models.ForeignKey(
        Tenant,
        blank = False,
        help_text = 'Tenant this belongs to',
        null = True,
        on_delete = models.CASCADE,
        related_name = '+',
        validators = [
            validatate_organization_exists
        ],
        verbose_name = 'Tenant'
    )



    def get_tenant(self) -> Tenant:
        """ Return the models Tenancy

        This model can be safely over-ridden as long as it returns the models
        tenancy
        """
        return self.organization