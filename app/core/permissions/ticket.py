from access.permissions.tenancy import TenancyPermissions



class TicketPermission(
    TenancyPermissions
):
    """Ticket Permissions

    After checking Tenancy permissions, check if the user has permissions:

    - `import`

    - `triage`

    and update the viewset with the results.

    Args:
        TenancyPermissions (Permission): Tenancy Based Permissions
    """

    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)

        tenancy = self.get_tenancy(view = view)

        if tenancy:

            view._has_import = request.user.has_perm(
                permission = f'{view.model._meta.app_label}.import_{view.model._meta.model_name}',
                tenancy = self.get_tenancy(view = view)
            )

            view._has_triage = request.user.has_perm(
                permission = f'{view.model._meta.app_label}.triage_{view.model._meta.model_name}',
                tenancy = self.get_tenancy(view = view)
            )

        return has_permission