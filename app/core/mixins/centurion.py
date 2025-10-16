from django.conf import settings
from django.core.exceptions import (
    ValidationError
)
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

    _linked_model_kwargs: tuple[ tuple[ str ] ] = None
    """Used for linking existing parent model.

    This field is only used for sub-models.

    Note: Leave this field blank if you don't wish to link existing models.
    """

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



    def clean_fields(self, exclude=None):

        self.link_parent_model()

        return super().clean_fields(exclude)



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


    def link_parent_model(self):
        """Link Existing parent model.

        Using `model._linked_model_kwargs` as the model filter kwargs, attempt to locate an
        existing model that matches, if so, then don't create a new model, link the existing model.

        Raises:
            ValidationError: When attempting to link parent model and there is a missing model
                within the chain.
        """

        if(
            (
                self.id is not None
                and not self._state.adding
                and not self._linked_model_kwargs
            )
            or not self._is_submodel
            or self._base_model == self
        ):
            return


        model_notes = self.model_notes

        parent_models = self._meta.get_parent_list()
        parent_models.reverse()

        prev_found_model = None
        for parent_model in parent_models:    # Confirm sub-model chain has ALL models created

            if not parent_model._is_submodel or not parent_model._linked_model_kwargs:
                continue


            for kwargs in parent_model._linked_model_kwargs:

                model_kwargs = {}
                for kwarg in kwargs:

                    kwarg_value = getattr(self, kwarg)

                    if not kwarg_value:
                        continue


                    model_kwargs.update({
                        kwarg: kwarg_value
                    })


                if len( model_kwargs ) != len( kwargs ):
                    continue

            existing_model = parent_model.objects.filter(
                **model_kwargs
            ).first()

            if prev_found_model and not existing_model:
                raise ValidationError(
                    message = (
                        f'Found matching {prev_found_model._meta.model_name} [id: {prev_found_model.id}], '
                        f'however unable to link as no {parent_model._meta.model_name} exists for '
                        f'this {prev_found_model._meta.model_name}'
                        ),
                    code = 'linking_models_break_in_chain'
                )

            if existing_model:
                prev_found_model = existing_model


        parent_model = self._meta.pk.related_model

        linked_model_kwargs = parent_model._linked_model_kwargs

        if not linked_model_kwargs:
            return

        for kwargs in linked_model_kwargs:

            model_kwargs = {}
            for kwarg in kwargs:

                kwarg_value = getattr(self, kwarg)

                if not kwarg_value:
                    continue


                model_kwargs.update({
                    kwarg: kwarg_value
                })


            if len( model_kwargs ) != len( kwargs ):
                continue


            existing_contact = parent_model.objects.filter(
                **model_kwargs
            ).first()

            if existing_contact:

                parent_fields = parent_model._meta.get_fields(include_parents = True)

                for parent_field in parent_fields:

                    if(
                        parent_field.auto_created
                        or not parent_field.editable
                        or not hasattr(self, parent_field.name)
                        or type(parent_field) in [    # Related Fields
                            models.ManyToManyRel,
                            models.ManyToOneRel,
                            models.OneToOneRel,
                        ]
                        or parent_field.name in [
                            'created',
                            'id',
                            'model_notes',    # This field is amended below
                            'modified',
                        ]
                    ):
                        continue


                    current_field_data = getattr(self, parent_field.name, None)
                    existing_field_data = getattr(existing_contact, parent_field.name, None)

                    if current_field_data != existing_field_data:

                        setattr(self, parent_field.name, existing_field_data)


                setattr(self, self._meta.pk.name, existing_contact)

                if model_notes:

                    if existing_contact.model_notes:

                        self.model_notes = existing_contact.model_notes + str( '\n\n' + model_notes )

                    else:

                        self.model_notes = model_notes


                self._state.adding = False

                break    # found a match process no further



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

            try:

                self._before = type(self).objects.get( id = self.id ).get_audit_values() or {}

            except models.ObjectDoesNotExist as e:
                self._before = {}


        super().save(force_insert=force_insert, force_update=force_update,
            using=using, update_fields=update_fields
        )
