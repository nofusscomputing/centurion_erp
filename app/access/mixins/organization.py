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



    parent_model_pk_kwarg: str = 'pk'
    """Parent Model kwarg

    This value is used to define the kwarg that is used as the parent objects primary key (pk).
    """
