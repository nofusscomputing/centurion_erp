from django.db import models



class CommonManager(
    models.Manager
):
    """Common Access Manager

    This manager contains the common functions required for ALL managers.
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


        if manager._permission:

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
