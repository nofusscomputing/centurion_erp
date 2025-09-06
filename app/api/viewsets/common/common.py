import django
import importlib
import logging
import rest_framework

from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import viewsets

from core.mixins.centurion import Centurion

from api.permissions.default import DefaultDenyPermission
from api.react_ui_metadata import ReactUIMetadata



class Create(
    viewsets.mixins.CreateModelMixin
):


    def create(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None
        instance = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            try:

                response = super().create(request = request, *args, **kwargs)

            except Exception as e:

                if not isinstance(e, APIException):

                    e = self._django_to_api_exception(e)

                if not isinstance(e, rest_framework.exceptions.ValidationError):

                    raise e

                is_unique = False
                for field, code in e.get_codes().items():

                    if 'unique' in code[0]:
                        is_unique = True


                if not is_unique:
                    raise e


                instance = self.model.objects.user(
                    user = self.request.user, permission = self._permission_required
                ).get( organization = request.data['organization'])

            # Always return using the ViewSerializer
            serializer_module = importlib.import_module(self.get_serializer_class().__module__)

            view_serializer = getattr(serializer_module, self.get_view_serializer_name())

            if(
                # response.data['id'] is not None
                response is not None
                and instance is None
            ):

                instance = response.data.serializer.instance


            serializer = view_serializer(
                instance,
                context = {
                    'request': request,
                    'view': self,
                },
            )

            serializer_data = serializer.data

            if response is None:

                headers = self.get_success_headers(serializer.data)
                status_code = rest_framework.status.HTTP_200_OK

            else:

                headers = response.headers
                status_code = response.status_code


            # Mimic ALL details from DRF response except serializer
            response = Response(
                data = serializer_data,
                status = status_code,
                # template_name = response.template_name,
                headers = headers,
                # exception = response.exception,
                # content_type = response.content_type,
            )

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )

        if hasattr(self.model, 'context'):

            self.model.context = { 'logger': None }

        return response



class Destroy(
    viewsets.mixins.DestroyModelMixin
):


    def destroy(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            response = super().destroy(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )


        if hasattr(self.model, 'context'):

            self.model.context = { 'logger': None }

        return response




class List(
    viewsets.mixins.ListModelMixin
):


    def list(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            response = super().list(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )

        if hasattr(self.model, 'context'):

            self.model.context = { 'logger': None }

        return response


# class PartialUpdate:




class Retrieve(
    viewsets.mixins.RetrieveModelMixin
):


    def retrieve(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            response = super().retrieve(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )

        if hasattr(self.model, 'context'):

            self.model.context = { 'logger': None }

        return response



class Update(
    viewsets.mixins.UpdateModelMixin
):


    def partial_update(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            response = super().partial_update(request = request, *args, **kwargs)

            if str(response.status_code).startswith('2'):
                # Always return using the ViewSerializer
                serializer_module = importlib.import_module(self.get_serializer_class().__module__)

                view_serializer = getattr(serializer_module, self.get_view_serializer_name())

                serializer = view_serializer(
                    response.data.serializer.instance,
                    context = {
                        'request': request,
                        'view': self,
                    },
                )

                # Mimic ALL details from DRF response except serializer
                response = Response(
                    data = serializer.data,
                    status = response.status_code,
                    template_name = response.template_name,
                    headers = response.headers,
                    exception = response.exception,
                    content_type = response.content_type,
                )

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )

        if hasattr(self.model, 'context'):

            self.model.context = { 'logger': None }

        return response


    def update(self, request, *args, **kwargs):
        """Sainty override

        This function overrides the function of the same name
        in the parent class for the purpose of ensuring a 
        non-api exception will not have the API return a HTTP
        500 error.

        This function is a sanity check that if it triggers,
        (an exception occured), the user will be presented with
        a stack trace that they will hopefully report as a bug.

        HTTP status set to HTTP/501 so it's distinguishable from
        a HTTP/500 which is generally a random error that has not
        been planned for. i.e. uncaught exception
        """

        response = None

        try:

            if hasattr(self.model, 'context'):

                self.model.context.update({
                    self.model._meta.model_name: self.request.user
                })
                self.model.context['logger'] = self.get_log()

            response = super().update(request = request, *args, **kwargs)

            if str(response.status_code).startswith('2'):

                # Always return using the ViewSerializer
                serializer_module = importlib.import_module(self.get_serializer_class().__module__)

                view_serializer = getattr(serializer_module, self.get_view_serializer_name())

                serializer = view_serializer(
                    response.data.serializer.instance,
                    context = {
                        'request': request,
                        'view': self,
                    },
                )

                # Mimic ALL details from DRF response except serializer
                response = Response(
                    data = serializer.data,
                    status = response.status_code,
                    template_name = response.template_name,
                    headers = response.headers,
                    exception = response.exception,
                    content_type = response.content_type,
                )

        except Exception as e:

            if not isinstance(e, APIException):

                e = self._django_to_api_exception(e)

            if hasattr(e, 'status_code'):
                response = Response(
                    data = e.get_full_details(),
                    status = e.status_code
                )

            else:
                response = Response(
                    data = {
                        e.__class__.__name__: str(e)
                    },
                    status = 500
                )

        if hasattr(self.model, 'context'):

            self.model.context['logger'] = None
            del self.model.context[self.model._meta.model_name]

        return response



class CommonViewSet(
    viewsets.ViewSet
):
    """Common ViewSet class

    This class is to be inherited by ALL viewsets.

    Args:
        viewsets (class): Django Rest Framework base class.
    """

    _permission_required: str = None
    """Cached Permissions required"""

    _queryset: models.QuerySet = None
    """View Queryset

    Cached queryset
    """


    def _django_to_api_exception( self, ex ):
        """Convert Django exception to DRF Exception

        Args:
            exc (Django.core.exceptions.*): Django exception to convert

        Raises:
            rest_framework.exceptions.ValidationError: Exception to return

        Returns:
            None: Exception not converted
        """

        rtn_exception = None

        if(
            isinstance(ex, django.core.exceptions.ObjectDoesNotExist)
            or isinstance(ex, django.http.Http404)
        ):

            exc = rest_framework.exceptions.NotFound(ex.args)

        elif isinstance(ex, django.core.exceptions.PermissionDenied):


            exc = rest_framework.exceptions.PermissionDenied(ex.error_dict)

        elif isinstance(ex, django.core.exceptions.ValidationError):


            exc = rest_framework.exceptions.ValidationError(ex.error_dict)

        else:

            exc = APIException(
                detail = f'20250704-Unknown Exception Type. Unable to convert. Please report this error as a bug. msg was {ex.msg}',
                code = 'unknown_exception'
            )

        try:

            raise exc

        except Exception as e:

            return e




    @property
    def allowed_methods(self):
        """Allowed HTTP Methods

        _Optional_, HTTP Methods allowed for the `viewSet`.

        Returns:
            list: Allowed HTTP Methods
        """

        return super().allowed_methods


    back_url: str = None
    """Back URL
    _Optional_, if specified will be added to view metadata for use for ui.
    """


    documentation: str = None
    """ Viewset Documentation URL

    _Optional_, if specified will be add to list view metadata
    """

    _log: logging.Logger = None
    
    def get_log(self):

        if self._log is None:

            self._log = settings.CENTURION_LOG.getChild( suffix = self.model._meta.app_label)

        return self._log


    metadata_class = ReactUIMetadata
    """ Metadata Class

    _Mandatory_, required so that the HTTP/Options method is populated with the data
    required to generate the UI.
    """

    metadata_markdown: bool = False
    """Query for item within markdown and add to view metadata
    
    **Note:** This is not required for detail view as by default the metadata
    is always gathered.
    """

    _model_documentation: str = None
    """Cached Model Documentation URL"""

    model_documentation: str = None
    """User Defined Model Documentation URL

    _Optional_, if specified will be add to detail view metadata"""

    page_layout: list = []
    """ Page layout class

    _Optional_, used by metadata to add the page layout to the HTTP/Options method
    for detail view, Enables the UI can setup the page layout.
    """

    permission_classes = [ DefaultDenyPermission ]
    """Permission Class

    _Mandatory_, Permission check class
    """

    table_fields: list = []
    """ Table layout list

    _Optional_, used by metadata for the table fields and added to the HTTP/Options
    method for detail view, Enables the UI can setup the table.
    """

    view_description: str = None

    view_name: str = None

    def get_back_url(self) -> str:
        """Metadata Back URL

        This URL is an optional URL that if required the view must
        override this method. If the URL for a back operation
        is not the models URL, then this method is used to return
        the URL that will be used.

        Defining this URL will predominatly be for sub-models. It's
        recommended that the `reverse` function
        (rest_framework.reverse.reverse) be used with a `request`
        object.

        Returns:
            str: Full url in format `<protocol>://<doman name>.<tld>/api/<API version>/<model url>`
        """

        return None


    def get_model_documentation(self) -> str:
        """Generate Documentation Path

        Documentation paths can be added in the following locations in priority of order (lower number is higher priority):

        1. `<viewset>.documentation`

        2. `<model>.documentation`

        3. Auto-magic generate using app label and model name

        Returns:
            str: Path to documentation
        """

        if not self._model_documentation:

            if getattr(self, 'documentation', None):

                self._model_documentation = self.documentation

            elif getattr(self.model, 'documentation', None):

                self._model_documentation = self.model.documentation

            elif getattr(self.model, '_meta', None):

                self._model_documentation = self.model._meta.app_label + '/' + str(
                    self.model._meta.verbose_name).lower().replace(' ', '_')


        return self._model_documentation



    def get_page_layout(self):

        if len(self.page_layout) < 1:

            if hasattr(self, 'model'):

                if hasattr(self.model, 'page_layout'):

                    self.page_layout = self.model.page_layout

                else:

                    self.page_layout = []

        return self.page_layout



    def get_queryset(self):

        if self._queryset is None:

            if(
                issubclass(self.model, Centurion)
                and hasattr(self.model.objects, 'user')
            ):

                self._queryset = self.model.objects.user(
                    user = self.request.user,
                    permission = self.get_permission_required()
                ).all()

            else:

                self._queryset = self.model.objects.all()

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


            self._queryset = self._queryset.filter( **qs_filter  )


        return self._queryset



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
            or getattr(self.request, 'method', '') == 'POST'
        ):

            view_action = 'add'

        elif (
            self.action == 'partial_update'
            or self.action == 'update'
            or getattr(self.request, 'method', '') == 'PATCH'
            or getattr(self.request, 'method', '') == 'PUT'
        ):

            view_action = 'change'

        elif(
            self.action == 'destroy'
            or getattr(self.request, 'method', '') == 'DELETE'
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



    def get_return_url(self) -> str:
        """Metadata return URL

        This URL is an optional URL that if required the view must
        override this method. If the URL for a cancel operation
        is not the models URL, then this method is used to return
        the URL that will be used.

        Defining this URL will predominatly be for sub-models. It's
        recommended that the `reverse` function
        (rest_framework.reverse.reverse) be used with a `request`
        object.

        Returns:
            str: Full url in format `<protocol>://<doman name>.<tld>/api/<API version>/<model url>`
        """

        return None


    def get_table_fields(self):

        if len(self.table_fields) < 1:

            if hasattr(self, 'model'):

                if hasattr(self.model, 'table_fields'):

                    self.table_fields = self.model.table_fields

                else:

                    self.table_fields = []

        return self.table_fields


    def get_view_description(self, html=False) -> str:

        if not self.view_description:

            self.view_description = ""
        
        if html:

            return mark_safe(f"<p>{self.view_description}</p>")

        else:

            return self.view_description


    def get_view_name(self):

        if self.view_name is not None:

            return self.view_name

        if getattr(self, 'model', None):

            if self.detail:

                self.view_name = str(self.model._meta.verbose_name)
            
            else:

                self.view_name = str(self.model._meta.verbose_name_plural)

        return self.view_name




class ModelViewSetBase(
    CommonViewSet
):


    filterset_fields: list = []
    """Fields to use for filtering the query

    _Optional_, if specified, these fields can be used to filter the API response
    """

    lookup_value_regex = '[0-9]+'
    """PK value regex"""

    model: object = None
    """Django Model
    _Mandatory_, Django model used for this view.
    """

    search_fields:list = []
    """ Search Fields

    _Optional_, Used by API text search as the fields to search.
    """

    serializer_class = None
    """Serializer class to use,
    
    If not used, use get_serializer_class function and cache the class here.
    """

    view_serializer_name: str = None
    """Cached model view Serializer name"""


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '_') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ', '_') + 'ModelSerializer']


        return self.serializer_class



    def get_view_serializer_name(self) -> str:
        """Get the Models `View` Serializer name.

        Override this function if required and/or the serializer names deviate from default.

        Returns:
            str: Models View Serializer Class name
        """

        if self.view_serializer_name is None:

            self.view_serializer_name = self.get_serializer_class().__name__.replace('ModelSerializer', 'ViewSerializer')

        return self.view_serializer_name



class CommonModelViewSet(
    ModelViewSetBase,
    Create,
    Retrieve,
    Update,
    Destroy,
    List,
    viewsets.ModelViewSet,
):

    pass



class CommonSubModelViewSet_ReWrite(
    CommonModelViewSet,
):
    """Temp class for SubModelViewSet

    This class contains the changed objects from parent `SubModelViewSet`. On
    all models be re-written, this class can be collapsed into its parent
    and replacing with the objects in this class
    """

    base_model = None
    """Model that is the base of this sub-model"""

    model_kwarg: str = None
    """Kwarg name for the sub-model"""

    model_suffix: str = None
    """Model Suffix

    This Value is added to `<model>._meta.model_name` when locating the models
    name. This field will normally not be required, except in the case of some
    sib-models.
    """


    @property
    def model(self):


        if getattr(self, '_model', None) is not None:

            return self._model

        model_kwarg = None

        if hasattr(self, 'kwargs'):

            model_kwarg = self.kwargs.get(self.model_kwarg, None)

        if model_kwarg:

            if self.model_suffix:

                model_kwarg = model_kwarg + self.model_suffix

            self._model = self.related_objects(self.base_model, model_kwarg)

        else:

            self._model = self.base_model


        return self._model


    def related_objects(self, model, model_kwarg):
        """Recursive relate_objects fetch

        Fetch the model where <model>._meta.model_name matches the
        model_kwarg value.

        Args:
            model (django.db.models.Model): The model to obtain the 
                related_model from.
            model_kwarg (str): The URL Kwarg of the model.

        Returns:
            Model: The model for the ViewSet
        """

        related_model = None

        if model_kwarg:

            is_nested_lookup = False

            for related_object in model._meta.related_objects:

                if(
                    getattr(
                            related_object.related_model._meta,'model_name', ''
                        ) == self.base_model._meta.model_name
                    or not issubclass(related_object.related_model, self.base_model)
                    or getattr(
                            related_object.related_model._meta,'sub_model_type', ''
                        ) == getattr(self.base_model._meta,'sub_model_type', '-not-exist')
                ):
                    continue


                related_objects = getattr(related_object.related_model._meta, 'related_objects', [])

                if(
                    str(
                        related_object.related_model._meta.model_name
                    ).lower().replace(' ', '_') == model_kwarg
                    or str(
                        getattr(related_object.related_model._meta, 'sub_model_type', '-not-exist')
                    ).lower().replace(' ', '_') == model_kwarg
                ):

                    related_model = related_object.related_model
                    break

                elif related_objects:

                    related_model = self.related_objects(
                        model = related_object.related_model, model_kwarg = model_kwarg
                    )

                    is_nested_lookup = True

                    if not hasattr(related_model, '_meta'):

                        related_model = None

                    elif(
                        str(
                            getattr(related_model._meta, 'model_name', '')
                        ).lower().replace(' ', '_') == model_kwarg
                        or str(
                            getattr(related_model._meta, 'sub_model_type', '')
                        ).lower().replace(' ', '_') == model_kwarg
                    ):

                        break


        if related_model is None and not is_nested_lookup:

            related_model = self.base_model

        return related_model



    def get_serializer_class(self):

        serializer_name = self.base_model._meta.model_name

        if self.base_model != self.model:
                      
            serializer_name += '_' + str( self.kwargs[self.model_kwarg] )


        serializer_module = importlib.import_module(
            self.model._meta.app_label + '.serializers.' + str(
                serializer_name
            )
        )

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = getattr(serializer_module, 'ViewSerializer')


        else:

            self.serializer_class = getattr(serializer_module, 'ModelSerializer')


        return self.serializer_class



class CommonModelCreateViewSet(
    ModelViewSetBase,
    Create,
    viewsets.GenericViewSet,
):

    pass



class CommonModelListRetrieveDeleteViewSet(
    ModelViewSetBase,
    List,
    Retrieve,
    Destroy,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to delete and view ONLY!"""

    pass



class CommonModelRetrieveUpdateViewSet(
    ModelViewSetBase,
    Retrieve,
    Update,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to update and view ONLY!"""

    pass



class CommonReadOnlyModelViewSet(
    ModelViewSetBase,
    Retrieve,
    List,
    viewsets.GenericViewSet,
):


    pass



class CommonReadOnlyListModelViewSet(
    ModelViewSetBase,
    List,
    viewsets.GenericViewSet,
):


    pass



# class AuthUserReadOnlyModelViewSet(
#     CommonReadOnlyModelViewSet
# ):
#     """Authenticated User Read-Only Viewset

#     Use this class if the model only requires that the user be authenticated
#     to obtain view permission.

#     Args:
#         ReadOnlyModelViewSet (class): Read-Only base class
#     """

#     permission_classes = [
#         IsAuthenticated,
#     ]


# class IndexViewset(
#     ModelViewSetBase,
# ):

#     permission_classes = [
#         IsAuthenticated,
#     ]


# class StaticPageNumbering(
#     pagination.PageNumberPagination
# ):
#     """Enforce Page Numbering

#     Enfore results per page min/max to static value that cant be changed.
#     """

#     page_size = 20

#     max_page_size = 20



# class PublicReadOnlyViewSet(
#     ReadOnlyListModelViewSet
# ):
#     """Public Viewable ViewSet

#     User does not need to be authenticated. This viewset is intended to be
#     inherited by viewsets that are intended to be consumed by unauthenticated
#     public users.

#     URL **must** be prefixed with `public`

#     Args:
#         ReadOnlyModelViewSet (ViewSet): Common Read-Only Viewset
#     """

#     pagination_class = StaticPageNumbering

#     permission_classes = [
#         IsAuthenticatedOrReadOnly,
#     ]

#     metadata_class = JSONAPIMetadata
