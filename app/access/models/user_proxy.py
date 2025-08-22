from django.apps import apps
from django.contrib.auth.models import Permission, AbstractUser
from django.core.exceptions import PermissionDenied

from access.models.tenant import Tenant



class CenturionUser(
    AbstractUser,
):
    """Centurion User

    A Multi-Tenant User wirh permission Checking.

    ToDo:
    - Add to Roles user field `related_name = roles`
    - Add to Roles group field `related_name = roles`
    # - have group lookup prefetch related roles__permissions
    - have user lookup prefetch related roles__permissions and groups__roles__permissions

    Args:
        User (Model): Django Base User
    """

    _tenancies: list[Tenant] = None

    _tenancies_int: list[int] = None

    _permissions: list[Permission] = None

    _permissions_by_tenancy: dict[ str, list[ Permission ] ] = None
    """Permissions by Tenancy

    `{ 'tenancy_{id}': [ Permission ] }`
    """

    # Update contact email field name so it's different to the user model.
    # EMAIL_FIELD = 'email'

    # REQUIRED_FIELDS = [
    #     EMAIL_FIELD,
    #     'f_name',
    #     'l_name',
    # ]

    class Meta:

        swappable = "AUTH_USER_MODEL"

        verbose_name = 'Centurion User'

        verbose_name_plural = 'Centurion Users'



    def get_full_name(self) -> str:
        return f'{self.entity_user.f_name} {self.entity_user.l_name}'



    def get_group_permissions(
        self, tenancy: bool = True
    ) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Args:
            tenancy (bool, optional): Return permission in list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        if self._tenancies is None:
            app_settings = apps.get_model(
                app_label = 'settings',
                model_name = 'appsettings',
            ).objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

            if app_settings.global_organization:
                self._tenancies = [ app_settings.global_organization ]
                self._tenancies_int = [ app_settings.global_organization.id ]
            else:
                self._tenancies = []
                self._tenancies_int = []

            if self._permissions is None:
                self._permissions = []

            if self._permissions_by_tenancy is None:
                self._permissions_by_tenancy = {}

            for group in self.groups.select_related('team__organization').prefetch_related('permissions__content_type').all():    # pylint: disable=E1133:not-an-iterable

                if group.team.organization not in self._tenancies:
                    self._tenancies += [ group.team.organization ]
                    self._tenancies_int += [ group.team.organization.id ]


                for permission in group.permissions.all():

                    view_permission = permission.content_type.app_label + '.' + permission.codename

                    if(
                        view_permission not in self._permissions
                    ):

                        self._permissions += [ view_permission ]


                    if 'tenancy_' + str(
                        group.team.organization.id) not in self._permissions_by_tenancy:

                        self._permissions_by_tenancy.update(
                            { 'tenancy_' + str(group.team.organization.id): []}
                        )


                    if(
                        view_permission not in self._permissions_by_tenancy['tenancy_' + str(
                            group.team.organization.id)]
                    ):

                        self._permissions_by_tenancy['tenancy_' + str(
                            group.team.organization.id)] += [ view_permission ]


        if tenancy:
            return self._permissions
        else:
            return self._permissions_by_tenancy





    def get_permissions(
        self, tenancy: bool = True
    ) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Args:
            tenancy (bool, optional): Return permission as tenancy list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        if self._tenancies is None:
            self.get_group_permissions()

        if tenancy:
            return self._permissions_by_tenancy

        return self._permissions



    def get_short_name() -> str:
        return self.entity_user.f_name



    def get_tenancies(self, int_list = False) -> list[ Tenant ] | list[ int ]:
        """Get the Tenancies the user is in.

        Args:
            int_list (bool, optional): Return Tenancy list as int values. Defaults to False.

        Returns:
            list[ Tenant ] | list[ int ]: All Tenancies the user is in.
        """

        if self._tenancies is None:

            self.get_group_permissions()


        if int_list:
            return self._tenancies_int

        return self._tenancies



    # def has_module_perms(self, app_label):    # is this needed?

    #     # if has app_label in perms

    #     # raise PermissionDenied
    #     return True



    def has_perm(
        self, permission: Permission, obj = None, tenancy: Tenant = None,
    ) -> bool:

        if self.is_superuser:
            return True

        if tenancy is None and obj is not None:
            tenancy = obj.get_tenant()

        if tenancy is not None:

            if f'tenancy_{tenancy.id}' not in self.get_permissions():
                return False


            if permission in self.get_permissions()[f'tenancy_{tenancy.id}']:
                return True


        else:

            if permission in self.get_permissions( tenancy = False ):
                return True

        return False



    def has_perms(
        self, permission_list: list[ Permission ], obj = None, tenancy: Tenant = None
    ) -> bool:

        for perm in permission_list:

            if not self.has_perm( perm, obj ):
                return False

        return True