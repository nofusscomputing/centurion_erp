from rest_framework.permissions import (
    DjangoModelPermissions,
    DjangoObjectPermissions
)



class CenturionModelPermissions(
    DjangoModelPermissions,
):
    """Centurion Model Permissions Mixin

    This is the base class for model permissions within Centurion.
    """

    _perms_map: dict[str, list[str]] | None = None

    _view_perms_map: dict[str, list[str]] | None = None

    _view_allowed_methods = []
    """Allowed Methods from ViewSet

    This property must be set during init.
    """


    @property
    def perms_map(self) -> dict[str, list[str]]:

        if len(self._view_allowed_methods) == 0:
            raise ValueError('cls._view_allowed_methods must contain the views methods.')


        if self._perms_map is None:

            self._perms_map = {
                'GET': [
                    '%(app_label)s.view_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('GET', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'OPTIONS': [
                    '%(app_label)s.view_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('OPTIONS', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'HEAD': [
                    '%(app_label)s.view_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('HEAD', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'POST': [
                    '%(app_label)s.add_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('POST', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'PUT': [
                    '%(app_label)s.change_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('PUT', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'PATCH': [
                    '%(app_label)s.change_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('PATCH', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
                'DELETE': [
                    '%(app_label)s.delete_%(model_name)s',
                    *(
                        getattr(self, '_view_perms_map', {}).get('DELETE', [] )
                        if self._view_perms_map is not None
                        else []
                    )
                ],
            }

            self._perms_map = { method: self._perms_map[method] for method in self._view_allowed_methods }

        return self._perms_map


    def permission_allowed_finaliser(self, view, user = None ) -> bool:
        """Perform any final actions

        Intent for this fn is that any final actions to be conducted prior
        to exiting/leaving the permission class.

        Args:
            view (ViewSet): ViewSet to be updated.
            user (CenturionUser): Update the allowed_methods to match the users
                 permissions.

        Returns:
            True (bool): Always returns true.
        """


        kwargs = {
            'app_label': view.model._meta.app_label,
            'model_name': view.model._meta.model_name
        }

        _perms_map = {    # Expand variables
                method: [
                    perm % kwargs for perm in perms
                ]
                    for method, perms in self.perms_map.items()
        }

        if user:

            view.allowed_methods = [
                method for method in view.allowed_methods
                    if user.has_perms(
                        permission_list = _perms_map.get(method, None),
                    )
            ]

        else:

            view.allowed_methods = [
                method for method in view.allowed_methods
                    if _perms_map.get(method, None) is not None
            ]

        return True


    def has_permission(self, request, view):
        raise NotImplementedError('This function must be implemented within your class')


class CenturionObjectPermissions(
    CenturionModelPermissions,
    DjangoObjectPermissions,
):
    """Centurion Object Permissions Mixin
    
    This is the base class for object permissions within Centurion.
    """
    pass


    def has_object_permission(self, request, view, obj):
        raise NotImplementedError('This function must be implemented within your class')
