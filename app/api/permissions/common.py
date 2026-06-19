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


    @property
    def perms_map(self) -> dict[str, list[str]]:


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

        return self._perms_map



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
