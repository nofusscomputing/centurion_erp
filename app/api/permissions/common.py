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


    @property
    def perms_map(self) -> dict[str, list[str]]:

        default: dict[str, list[str]] = {
            'GET': [
                '%(app_label)s.view_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'GET', []
                )
            ],
            'OPTIONS': [
                '%(app_label)s.view_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'OPTIONS', []
                )
            ],
            'HEAD': [
                '%(app_label)s.view_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'HEAD', []
                )
            ],
            'POST': [
                '%(app_label)s.add_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'POST', []
                )
            ],
            'PUT': [
                '%(app_label)s.change_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'PUT', []
                )
            ],
            'PATCH': [
                '%(app_label)s.change_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'PATCH', []
                )
            ],
            'DELETE': [
                '%(app_label)s.delete_%(model_name)s',
                *getattr(self, '_perms_map', {}).get(
                    'DELETE', []
                )
            ],
        }

        return default



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
