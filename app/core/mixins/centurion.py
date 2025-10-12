from django.conf import settings
from django.db import models

from rest_framework.reverse import reverse



class Centurion(
    models.Model
):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.context = {
            'logger': None,
            self._meta.model_name: None
        }


    class Meta:

        abstract = True


    _audit_enabled: bool = True
    """Should this model have audit history kept"""

    _base_model: models.Model = None
    """Base model for this sub-model
    
    This should be set to the first model within the chain of models.
    """

    _is_submodel: bool = False
    """This model a sub-model"""

    _notes_enabled: bool = True
    """Should a table for notes be created for this model"""

    _ticket_linkable: bool = True
    """Should this model be linkable to a ticket"""

    app_namespace: str = None
    """URL Application namespace.

    **Note:** This attribute is a temp attribute until all models urls return
    to their own `urls.py` file from `api/urls_v2.py`.
    """

    context = { 'logger': None }
    """ Model Context

    Generally model usage will be from an API serializer, Admin Site or
    a management command. These sources are to pass through and set this
    context. The keys are:

    !!! warning
        Failing to specify the user will prevent the tenancy manager from
        being multi-tenant. As such, the results retured will not be
        restricted to the users tenancy

    returns:
        logger (logging.Logger): Instance of a logger for logging.
        model_name (User): The user that is logged into the system

    Context for actions within the model.
    """

    model_tag: str = None
    """Model Tag
    
    String that is used as this models tag. Used within ticketing for linking a
    model to a ticket and wihin markdown for referencing a model.
    """

    url_model_name: str = None
    """URL Model Name override

    Optionally use this attribute to set the model name for the url `basename`,
    i.e. `_api_<url_model_name>`
    """


    def delete(self, using = None, keep_parents = None):
        """Delete Centurion Model

        If a model has `_audit_enabled = True`, audit history is populated and
        ready to be saved by the audit system (save signal.). 

        Args:
            using (_type_, optional): _description_. Defaults to None.
            keep_parents (bool, optional): Keep parent models. Defaults to the
                value if is_submodel so as not to delete parent models.
        """

        if keep_parents is None:
            keep_parents = self._is_submodel

        if self._audit_enabled:

            self._after = {}

            self._before = self.get_audit_values()


        super().delete(using = using, keep_parents = keep_parents)



    def full_clean(self, exclude = None,
        validate_unique = True, validate_constraints = True
    ) -> None:

        super().full_clean(
            exclude = exclude,
            validate_unique = validate_unique,
            validate_constraints = validate_constraints
        )


    def get_app_namespace(self) -> str:
        """Fetch the Application namespace if specified.

        **Note:** This attribute is a temp attribute until all models urls return
        to their own `urls.py` file from `api/urls_v2.py`.

        Returns:
            str: Application namespace suffixed with colin `:`
            None: No application namespace found.
        """

        if not self.app_namespace:
            return None

        app_namespace = self.app_namespace

        return str(app_namespace)


    def get_audit_values(self) -> dict:
        """Retrieve the field Values

        Currently ensures only fields are present.

        **ToDo:** Update so the dict that it returns is a dict of dict where each dict
        is named after the actual models the fields come from and it contains
        only it's fields.

        Returns:
            dict: Model fields
        """

        data = self.__dict__.copy()

        clean_data: dict = {}

        for field in self._meta.fields:

            if hasattr(self, field.name):

                clean_data.update({
                    field.name: getattr(self, field.name)
                })


        return clean_data



    def get_after(self) -> dict:
        """Audit Data After Change

        Returns:
            dict: All model fields after the data changed
        """
        return self._after



    def get_before(self) -> dict:
        """Audit Data Before Change

        Returns:
            dict: All model fields before the data changed
        """
        return self._before



    def get_history_model_name(self) -> str:
        """Get the name for the History Model

        Returns:
            str: Name of the history model (`<model class name>AuditHistory`)
        """

        return f'{self._meta.object_name}AuditHistory'



    def get_organization(self):
        """Return the objects organization"""
        return self.organization



    def get_related_field_name(self) -> str:
        """Related model field name.

        Get the name of the attribute within this model for it's related model.
        This method is normally only used for sub-models.

        Returns:
            str: Field name of the related model.
            empty string (str): There is not related model.
        """

        if self._base_model:

            meta = getattr(self, '_meta')


            for related_object in getattr(meta, 'related_objects', []):

                if not issubclass(related_object.related_model, self._base_model):

                    continue


                if getattr(self, related_object.name, None):

                    if( 
                        not str(related_object.name).endswith('history')
                        and not str(related_object.name).endswith('notes')
                    ):

                        return related_object.name


        return ''


    def get_related_model(self):
        """Recursive model Fetch

        Returns the lowest model found in a chain of inherited models.

        Returns:
            models.Model: Lowset model found in inherited model chain
            self: Model is not a sub-model or this sub-model was directly accessed.
        """

        related_model_name = self.get_related_field_name()

        related_model = getattr(self, related_model_name, None)

        if related_model is None:

            related_model = self

        elif hasattr(related_model, 'get_related_field_name'):

            if related_model.get_related_field_name() != '':

                related_model = related_model.get_related_model()


        return related_model



    def get_url(
        self, relative: bool = False, api_version: int = 2, many = False, request: any = None
    ) -> str:
        """Return the models API URL

        Args:
            relative (bool, optional): Return the relative URL for the model. Defaults to False.
            api_version (int, optional): API Version to use. Defaults to `2``.
            request (any, optional): Temp and unused attribute until rest of
                codebase re-written not to pass through.

        Returns:
            str: API URL for the model
        """

        namespace = f'v{api_version}'

        model = self.get_related_model()

        if model.get_app_namespace():
            namespace = namespace + ':' + model.get_app_namespace()


        url_basename = f'{namespace}:_api_{model._meta.model_name}'

        if model.url_model_name:

            url_basename = f'{namespace}:_api_{model.url_model_name}'

        if model._is_submodel:

            url_basename += '_sub'


        if many:

            url_basename += '-list'

        else:

            url_basename += '-detail'


        url = reverse( viewname = url_basename, kwargs = model.get_url_kwargs( many = many ) )

        if not relative:

            url = settings.SITE_URL + url


        return url



    def get_url_kwargs(self, many = False) -> dict:
        """Get URL Kwargs

        Fecth the kwargs required for building a models URL using the reverse
        method.

        **Note:** It's advisable that if you override this function, that you
        call it's super, so as not to duplicate code. That way each override
        builds up[on the parent `get_url_kwargs` function.

        Returns:
            dict: Kwargs required for reverse function to build a models URL.
        """

        kwargs = {}

        model = self.get_related_model()

        if model._is_submodel:

            kwargs.update({
                'model_name': str( model._meta.model_name ),
            })

        if many:

            return kwargs

        else:

            kwargs.update({
                'pk': model.id
            })

            return kwargs



    def save(self, force_insert = False, force_update = False, using = None, update_fields = None):
        """Save Centurion Model

        This Save ensures that `full_clean()` is called so that prior to the
        model being saved to the database, it is valid.

        If a model has `_audit_enabled = True`, audit history is populated and
        ready to be saved by the audit system (save signal.). 
        """

        self.full_clean(
            exclude = None,
            validate_unique = True,
            validate_constraints = True
        )

        if self._audit_enabled and type(self).context.get(self._meta.model_name, None):

            self._after = self.get_audit_values()

            if self.id:

                self._before = type(self).objects.get( id = self.id ).get_audit_values()

            else:

                self._before = {}


        super().save(force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields
        )
