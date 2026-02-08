from django.apps import apps
from django.contrib.auth.models import Permission, AbstractUser

from access.models.tenant import Tenant



class CenturionUser(
    AbstractUser,
):
    """Centurion User

    A Multi-Tenant User wirh permission Checking.

    Users authorization is by role. No permissions that are assigned to the user or group
    are to be considered as a users permissions. That is due to requiring an tenancy for
    the permission to be assigned to. This is done by assigning the permissions to a role,
    which has a tenancy. The role is then assigned to either a user or group.

    Args:
        User (Model): Django Base User
    """

    _global_organization = None

    _group_permissions: bool = False

    _tenancies: list[Tenant] = None

    _tenancies_int: list[int] = None

    _permissions: list[Permission] = None

    _permissions_by_tenancy: dict[ str, list[ Permission ] ] = None
    """Permissions by Tenancy

    `{ 'tenancy_{id}': [ Permission ] }`
    """

    _user_permissions: bool = False

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



    def __int__(self) -> int:
        return int(self.id)



    def get_entity(self):
        """Get Users Entity

        Returns:
            CenturionUser: Employee Centurion User account
            None: No User Account found.
        """

        employee = getattr(self, 'employee', None)

        if employee:
            return employee

        return None



    def get_group_permissions(
        self, tenancy: bool = True
    ) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Group Permissions

        Obtains all permissions and tenancies from the roles assigned to groups the
        use is a part of.

        Args:
            tenancy (bool, optional): Return permission in list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        if not self._group_permissions:

            if self._tenancies is None:
                self._tenancies = []

            if self._tenancies_int is None:
                self._tenancies_int = []

            if self._permissions is None:
                self._permissions = []

            if self._permissions_by_tenancy is None:
                self._permissions_by_tenancy = {}


            app_settings = apps.get_model(
                app_label = 'settings',
                model_name = 'appsettings',
            ).objects.select_related('global_organization').filter(
                owner_organization = None
            )[0]

            if app_settings.global_organization:
                self._tenancies = [ app_settings.global_organization ]
                self._tenancies_int = [ app_settings.global_organization.id ]
                self.global_organization = app_settings.global_organization


            for group in self.groups.prefetch_related(
                'roles__permissions__content_type','roles__organization'
            ):

                for role in group.roles.all():

                    if role.organization not in self._tenancies:
                        self._tenancies += [ role.organization ]
                        self._tenancies_int += [ role.organization.id ]


                    if 'tenancy_' + str(
                        role.organization.id) not in self._permissions_by_tenancy:

                        self._permissions_by_tenancy.update(
                            { 'tenancy_' + str(role.organization.id): []}
                        )


                    for permission in role.permissions.all():

                        view_permission = str(
                            permission.content_type.app_label + '.' + permission.codename
                        )

                        if(
                            view_permission not in self._permissions
                        ):

                            self._permissions += [ view_permission ]


                        if(
                            view_permission not in self._permissions_by_tenancy['tenancy_' + str(
                                role.organization.id)]
                        ):

                            self._permissions_by_tenancy['tenancy_' + str(
                                role.organization.id)] += [ view_permission ]

        self._group_permissions = True

        if tenancy:
            return self._permissions_by_tenancy

        return self._permissions



    def get_permissions(
        self, tenancy: bool = True
    ) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Obtains all permissions and tenancies from the roles assigned to the user.

        Args:
            tenancy (bool, optional): Return permission as tenancy list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        if not self._group_permissions:
            self.get_group_permissions()

        if not self._user_permissions:
            self.get_user_permissions()

        if tenancy:
            return self._permissions_by_tenancy

        return self._permissions



    def get_tenancies(self, int_list = False) -> list[ Tenant ] | list[ int ]:
        """Get the Tenancies the user is in.

        Args:
            int_list (bool, optional): Return Tenancy list as int values. Defaults to False.

        Returns:
            list[ Tenant ] | list[ int ]: All Tenancies the user is in.
        """

        if self._tenancies is None:
            if not self._group_permissions:
                self.get_group_permissions()

            if not self._user_permissions:
                self.get_user_permissions()


        if int_list:
            return self._tenancies_int

        return self._tenancies




    def get_user_permissions(
        self, tenancy: bool = True
    ) -> dict[ str, list[ Permission ] ] | list[ Permission ]:
        """ Get the Users Permissions

        Args:
            tenancy (bool, optional): Return permission in list. Defaults to True.

        Returns:
            dict[ str, list[ Permission ] ]: Permissions listed by tenancy
            list[ Permission ]: All Permissions
        """

        if not self._user_permissions:

            if self._tenancies is None:
                self._tenancies = []

            if self._tenancies_int is None:
                self._tenancies_int = []

            if self._permissions is None:
                self._permissions = []

            if self._permissions_by_tenancy is None:
                self._permissions_by_tenancy = {}

            for role in self.roles.prefetch_related('permissions__content_type', 'organization'):

                if role.organization not in self._tenancies:
                    self._tenancies += [ role.organization ]
                    self._tenancies_int += [ role.organization.id ]


                for permission in role.permissions.all():

                    view_permission = permission.content_type.app_label + '.' + permission.codename

                    if(
                        view_permission not in self._permissions
                    ):

                        self._permissions += [ view_permission ]


                    if(
                        'tenancy_' + str(
                            role.organization.id) not in self._permissions_by_tenancy
                    ):

                        self._permissions_by_tenancy.update(
                            { 'tenancy_' + str(role.organization.id): []}
                        )


                    if(
                        view_permission not in self._permissions_by_tenancy['tenancy_' + str(
                            role.organization.id)]
                    ):

                        self._permissions_by_tenancy['tenancy_' + str(
                            role.organization.id)] += [ view_permission ]

        self._user_permissions = True

        if tenancy:
            return self._permissions_by_tenancy
        else:
            return self._permissions



    def has_perm(
        self, permission: str, obj = None, tenancy: Tenant = None,
        tenancy_permission: bool = True
    ) -> bool:


        if tenancy is None and obj is None and tenancy_permission:
            raise ValueError('either an object or tanancy is required.')


        if tenancy is None and obj is not None:
            tenancy = obj.get_tenant()


        if tenancy is not None:

            if permission in self.get_permissions().get(f'tenancy_{tenancy.id}', []):
                return True

        else:

            if permission in self.get_permissions( tenancy = False ):
                return True


        return False



    def has_perms(
        self, permission_list: list[ str ], obj = None, tenancy: Tenant = None
    ) -> bool:

        has_perms = True

        if not isinstance(permission_list, list):
            raise TypeError(f'permissions list must be of type list, not type {type(permission_list)}')

        for perm in permission_list:

            if obj:

                if not self.has_perm( permission = perm, obj = obj ):
                    has_perms = False

            elif tenancy:

                if not self.has_perm( permission = perm, tenancy = tenancy ):
                    has_perms = False

            elif not obj and not tenancy:

                if not self.has_perm( permission = perm, tenancy_permission = False ):
                    has_perms = False

            else:
                has_perms = False

        return has_perms
