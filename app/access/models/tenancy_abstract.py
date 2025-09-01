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

    _permission = None

    _tenancies = None

    _user = None

    def user(self, user, permission):
        """Set-up for Tenancy Queryset

        This method sets up the manager with the users details so that the queryset
        only contains the data the user has access to.

        Args:
            user (CenturionUser): The user the Queryset is for
            permission (str): The ViewSet permission. use get_permission function.

        Returns:
            TenancyManager: Fresh TenancyManager instance
        """
        manager = self.__class__()
        manager._permission = permission
        manager._user = user

        manager.model = self.model
        manager._db = self._db

        manager._tenancies = []
        if getattr(manager._user, 'global_organization', None):
            manager._tenancies = [ int(manager._user.global_organization) ]


        for tenancy in manager._user.get_tenancies(int_list = False):
            if manager._user.has_perm(
                permission = manager._permission,
                tenancy = tenancy
            ):

                manager._tenancies += [ int(tenancy) ]

        return manager


    def get_queryset(self):
        """ Fetch the data

        It's assumed that the query method from the view/ViewSet has added the user object
        to the model under attribute `.context[<_meta.model_name>]` as that's the model the user is
        fetching for their query. It's done like this so that within code, a full query can
        be done without the data being filtered to the user in question.

        Returns:
            (queryset): **super user**: return unfiltered data.
            (queryset): **not super user**: return data from the stored unique organizations.
        """

        has_tenant_field = False

        if(
            getattr(self.model, 'organization', None) is not None
            or getattr(self.model, 'tenant', None) is not None
        ):
            has_tenant_field = True


            if getattr(self._user, 'id', None) and getattr(self._user, 'is_authenticated', False):


                if not self._user.is_superuser and self._tenancies:

                    return super().get_queryset().select_related('organization').filter(
                        models.Q(organization__in = self._tenancies)
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