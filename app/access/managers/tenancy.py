from django.db import models

from access.managers.common import CommonManager



class TenancyManager(
    CommonManager
):
    """Multi-Tennant Object Manager

    This manager specifically caters for the multi-tenancy features of Centurion ERP.
    """


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

        elif(
            getattr(self, '_user')
            and getattr(self.model._meta, 'model_name', None) == 'tenant'
            and self._tenancies
        ):

            return super().get_queryset().filter(
                        models.Q(id__in = self._tenancies)
                    )


        return super().get_queryset()
