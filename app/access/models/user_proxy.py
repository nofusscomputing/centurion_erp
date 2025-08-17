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

    # EMAIL_FIELD = 'email'    # Update contact email field name so it's different to the user model.

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



    def get_group_permissions(self, tenancy: bool = True) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Args:
            tenancy (bool, optional): Return permission in list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """
        
        for group in self.groups:    # pylint: disable=E1133:not-an-iterable

            for role in group.roles:
                pass

                # role.get_permissions()



    def get_permissions(self, tenancy: bool = True) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Args:
            tenancy (bool, optional): Return permission in list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        # also get group permissions. self.get_group_permissions()

        for role in self.roles:
            pass

            # role.get_permissions()

            # also populate `self._tenancies` and `self._tenancies_int`

        return []



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

            if self._permissions is None:
                self.get_permissions

            tenancies: list = []
            tenancies_int: list = []

            for role in self.roles:

                if role.organization in tenancies:
                    continue

                tenancies += [ role.organization ]
                tenancies_int += [ role.organization.id ]

            self._tenancies = tenancies
            self._tenancies_int = tenancies_int


        if as_int_list:
            return self._tenancies_int

        return self._tenancies



    def has_module_perms(self, app_label):    # is this needed?

        # if has app_label in perms

        raise PermissionDenied



    def has_perm(self, permission: Permission, obj = None, tenancy: Tenant = None) -> bool:

        if(
            obj is None
            and tenancy is None
        ):
            raise ValueError('Both obj and tenancy cant be None')

        if tenancy is None:
            tenancy = obj.organization

        # if self.has_tenancy_permission(perm, tenancy):
        # for tenancy, permissions in self.get_permissions().items()

        if tenancy is None:
            raise ValueError('tenancy cant be None')

        permissions = self.get_permissions()

        if f'tenancy_{tenancy.id}' not in permissions:
            raise PermissionDenied


        for tenancy, permissions in self.get_permissions().items():

            if(
                tenancy == f'tenancy_{tenancy.id}'
                and perm in permissions
            ):
                return True


        raise PermissionDenied



    def has_perms(self, permission_list: list[ Permission ], obj = None, tenancy: Tenant = None):

        for perm in perm_list:

            self.has_perm( perm, obj )

        return True