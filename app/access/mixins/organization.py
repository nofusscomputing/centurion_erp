from django.db import models



class OrganizationMixin:
    """Organization Tenancy Mixin

    This class is intended to be included in **ALL** View / Viewset classes as
    it contains the functions/methods required to conduct the permission
    checking.
    """



    def get_parent_obj(self):
        """ Get the Parent Model Object

        Use in views where the the model has no organization and the organization should be fetched from the parent model.

        Requires attribute `parent_model` within the view with the value of the parent's model class

        Returns:
            parent_model (Model): with PK from kwargs['pk']
        """

        return self.get_parent_model().objects.get(pk=self.kwargs[self.parent_model_pk_kwarg])


    _permission_required: str = None
    """Cached Permissions required"""


    def get_permission_required(self) -> str:
        """ Get / Generate Permission Required

        If there is a requirement that there be custom/dynamic permissions,
        this function can be safely overridden.

        Raises:
            ValueError: Unable to determin the view action

        Returns:
            str: Permission in format `<app_name>.<action>_<model_name>`
        """

        if self._permission_required:

            return self._permission_required


        if hasattr(self, 'get_dynamic_permissions'):

            self._permission_required = self.get_dynamic_permissions()

            if type(self._permission_required) is list:

                self._permission_required = self._permission_required[0]

            return self._permission_required


        view_action: str = None

        if(
            self.action == 'create'
            or getattr(self.request._stream, 'method', '') == 'POST'
        ):

            view_action = 'add'

        elif (
            self.action == 'partial_update'
            or self.action == 'update'
            or getattr(self.request._stream, 'method', '') == 'PATCH'
            or getattr(self.request._stream, 'method', '') == 'PUT'
        ):

            view_action = 'change'

        elif(
            self.action == 'destroy'
            or getattr(self.request._stream, 'method', '') == 'DELETE'
        ):

            view_action = 'delete'

        elif (
            self.action == 'list'
        ):

            view_action = 'view'

        elif self.action == 'retrieve':

            view_action = 'view'

        elif self.action == 'metadata':

            view_action = 'view'

        elif self.action is None:

            return False



        if view_action is None:

            raise ValueError('view_action could not be defined.')


        permission = self.model._meta.app_label + '.' + view_action + '_' + self.model._meta.model_name

        permission_required = permission


        self._permission_required = permission_required

        return self._permission_required


    parent_model_pk_kwarg: str = 'pk'
    """Parent Model kwarg

    This value is used to define the kwarg that is used as the parent objects primary key (pk).
    """
