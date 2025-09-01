from django.db import models

from access.models.tenancy import Tenant
from access.models.tenancy_abstract import TenancyAbstractModel
from access.permissions.tenancy import TenancyPermissions



class TenancyMixin:


    _obj_tenancy: Tenant = None

    parent_model: models.Model = None
    """ Parent Model

    This attribute defines the parent model for the model in question. The parent model when defined
    will be used as the object to obtain the permissions from.
    """

    parent_model_pk_kwarg: str = 'pk'
    """Parent Model kwarg

    This value is used to define the kwarg that is used as the parent objects primary key (pk).
    """

    permission_classes = [ TenancyPermissions ]
    """Permission Class

    _Mandatory_, Permission check class
    """

    _queryset: models.QuerySet = None
    """View Queryset

    Cached queryset
    """


    def get_parent_model(self):
        """Get the Parent Model

        This function exists so that dynamic parent models can be defined.
        They are defined by overriding this method.

        Returns:
            Model: Parent Model
        """

        return self.parent_model



    def get_parent_obj(self):
        """ Get the Parent Model Object

        Use in views where the the model has no organization and the organization should be fetched from the parent model.

        Requires attribute `parent_model` within the view with the value of the parent's model class

        Returns:
            parent_model (Model): with PK from kwargs['pk']
        """

        return self.get_parent_model().objects.get(pk=self.kwargs[self.parent_model_pk_kwarg])



    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        if issubclass(self.model, TenancyAbstractModel):

            self.queryset = self.model.objects.user(
                user = self.request.user,
                action = self._permission_required
            ).all()
        
        else:

            self.queryset = self.model.objects.all()

        qs_filter = {}

        if 'pk' in getattr(self, 'kwargs', {}):

            qs_filter.update({
                'pk': int( self.kwargs['pk'] )
            })

        if(
            getattr(self.model, '_is_submodel', False)
            and 'model_id' in self.kwargs
        ):

            qs_filter.update({
                'model_id': int( self.kwargs['model_id'] )
            })


        self.queryset = self.queryset.filter( **qs_filter  )


        return self.queryset
