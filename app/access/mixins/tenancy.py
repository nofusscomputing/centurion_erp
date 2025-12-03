from django.db import models

from access.models.tenancy import Tenant
from access.permissions.tenancy import TenancyPermissions



class TenancyMixin:


    _obj_tenancy: Tenant = None

    _queryset: models.QuerySet = None
    """View Queryset

    Cached queryset
    """

    parent_model: models.Model = None
    """ Parent Model

    This attribute defines the parent model for the model in question. The
    parent model when defined will be used as the object to obtain the
    permissions from.

    Generally this wont need to be defined. A use case for this is when you
    link two models. You would define the parent_model and ensure that the
    tenancy (`model.tenancy = parent_model.get_tenanncy()`) matches the parent.
    This should be done in (i.e. within `model.clean_fields()` )
    """

    parent_model_pk_kwarg: str = 'pk'
    """Parent Model kwarg

    This value is used to define the kwarg that is used as the parent objects primary key (pk).
    """

    permission_classes = [ TenancyPermissions ]
    """Permission Class

    _Mandatory_, Permission check class
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

        Use in views where the the model has no organization and the organization should be fetched
        from the parent model.

        Requires attribute `parent_model` within the view with the value of the parent's model class

        Returns:
            parent_model (Model): with PK from kwargs['pk']
        """

        return self.get_parent_model().objects.get(pk=self.kwargs[self.parent_model_pk_kwarg])
