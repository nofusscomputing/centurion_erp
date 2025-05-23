from django.core.exceptions import (
    ValidationError,
)
from django.db import models

from access.models.tenant import Tenant



class TenancyManager(
    models.Manager
):
    """Multi-Tennant Object Manager

    This manager specifically caters for the multi-tenancy features of Centurion ERP.
    """

    def get_queryset(self):
        """ Fetch the data

        When the model contains the user data, the query is filtered to their
        and the globally defined Tenancy only.

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        user = None    # When CenturionUser in use

        if hasattr(self.model, 'context'):

            user = self.model.context['user']


        has_tenant_field = False
        if hasattr(self.model, 'organization'):
            has_tenant_field = True


        if user:

            tencies = user.get_tenancies(int_list = True)

            if len(tenancies) > 0 and not request.user.is_superuser:

                if has_tenant_field:
                    return super().get_queryset().select_related('organization').filter(
                        models.Q(organization__in = tenancies)
                    )


                return super().get_queryset().select_related('organization').filter(
                    models.Q(organization__in = tenancies)
                )


        if has_tenant_field:
            return super().get_queryset().select_related('organization')


        return super().get_queryset()



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

    context: dict = {
        'logger': None,
        'user': None,
    }
    """ Model Context

    Context for actions within the model.
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
            raise ValidationError(
                code = 'required',
                message = 'You must provide an organization'
            )

    organization = models.ForeignKey(
        Tenant,
        blank = False,
        help_text = 'Tenant this belongs to',
        null = False,
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