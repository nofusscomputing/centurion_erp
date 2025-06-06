import importlib
import logging

from django.utils.safestring import mark_safe

from rest_framework import viewsets, pagination
from rest_framework_json_api.metadata import JSONAPIMetadata
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from access.mixins.organization import OrganizationMixin
from access.mixins.permissions import OrganizationPermissionMixin

from api.auth import TokenScheme
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

        try:

            response = super().create(request = request, *args, **kwargs)

            # Always return using the ViewSerializer
            serializer_module = importlib.import_module(self.get_serializer_class().__module__)

            view_serializer = getattr(serializer_module, self.get_view_serializer_name())

            if response.data['id'] is not None:

                serializer = view_serializer(
                    self.get_queryset().get( pk = int(response.data['id']) ),
                    context = {
                        'request': request,
                        'view': self,
                    },
                )

                serializer_data = serializer.data

            else:


                serializer_data = {}


            # Mimic ALL details from DRF response except serializer
            response = Response(
                data = serializer_data,
                status = response.status_code,
                template_name = response.template_name,
                headers = response.headers,
                exception = response.exception,
                content_type = response.content_type,
            )

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

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

            response = super().destroy(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

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

            response = super().list(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

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

            response = super().retrieve(request = request, *args, **kwargs)

        except Exception as e:

            if not isinstance(e, APIException):

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

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

            response = super().partial_update(request = request, *args, **kwargs)

            # Always return using the ViewSerializer
            serializer_module = importlib.import_module(self.get_serializer_class().__module__)

            view_serializer = getattr(serializer_module, self.get_view_serializer_name())

            serializer = view_serializer(
                self.queryset.get( pk = int(self.kwargs['pk']) ),
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

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

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

            response = super().update(request = request, *args, **kwargs)

            # Always return using the ViewSerializer
            serializer_module = importlib.import_module(self.get_serializer_class().__module__)

            view_serializer = getattr(serializer_module, self.get_view_serializer_name())

            serializer = view_serializer(
                self.queryset.get( pk = int(self.kwargs['pk']) ),
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

                response = Response(
                    data = {
                        'server_error': str(e)
                    },
                    status = 501
                )

                self.get_log().exception(e)

            else:

                response = Response(
                    data = e.detail,
                    status = e.status_code
                )

        return response



class CommonViewSet(
    OrganizationMixin,
    viewsets.ViewSet
):
    """Common ViewSet class

    This class is to be inherited by ALL viewsets.

    Args:
        OrganizationMixin (class): Contains the Authorization checks.
        viewsets (class): Django Rest Framework base class.
    """

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

            self._log = logging.getLogger('centurion.' + self.model._meta.app_label)

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

    permission_classes = [ OrganizationPermissionMixin ]
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

    queryset: object = None
    """View Queryset

    _Optional_, View model Query
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


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.queryset = self.model.objects.all()

        if 'pk' in getattr(self, 'kwargs', {}):

            self.queryset = self.queryset.filter( pk = int( self.kwargs['pk'] ) )


        return self.queryset



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



class ModelViewSet(
    ModelViewSetBase,
    Create,
    Retrieve,
    Update,
    Destroy,
    List,
    viewsets.ModelViewSet,
):

    pass



class SubModelViewSet(
    ModelViewSet,
):

    base_model = None
    """Model that is the base of this sub-model"""

    model_kwarg: str = None
    """Kwarg name for the sub-model"""


    @property
    def model(self):


        if getattr(self, '_model', None) is not None:

            return self._model

        model_kwarg = None

        if hasattr(self, 'kwargs'):

            model_kwarg = self.kwargs.get(self.model_kwarg, None)

        if model_kwarg:

            self._model = self.related_objects(self.base_model, model_kwarg)

        else:

            self._model = self.base_model

        return self._model


    def related_objects(self, model, model_kwarg):
        """Recursive relate_objects fetch

        Fetch the model where <model>._meta.sub_model_type matches the
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
                    getattr(related_object.related_model._meta,'sub_model_type', '' ) == self.base_model._meta.sub_model_type
                    or not issubclass(related_object.related_model, self.base_model)
                ):

                    continue


                related_objects = getattr(related_object.related_model._meta, 'related_objects', [])

                if(
                    str(
                        related_object.related_model._meta.sub_model_type
                    ).lower().replace(' ', '_') == model_kwarg
                ):

                    related_model = related_object.related_model
                    break
                
                elif related_objects:

                    related_model = self.related_objects(model = related_object.related_model, model_kwarg = model_kwarg)

                    is_nested_lookup = True



                    if not hasattr(related_model, '_meta'):

                        related_model = None

                    elif(
                        str(
                            getattr(related_model._meta, 'sub_model_type', '')
                        ).lower().replace(' ', '_') == model_kwarg
                    ):

                        break



        if related_model is None and not is_nested_lookup:

            related_model = self.base_model

        return related_model



    def get_serializer_class(self):

        serializer_name = self.base_model._meta.verbose_name.lower().replace(' ', '_')

        if self.base_model != self.model:
                      
            serializer_name += '_' + self.model._meta.sub_model_type


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





class ModelCreateViewSet(
    ModelViewSetBase,
    Create,
    viewsets.GenericViewSet,
):

    pass



class ModelListRetrieveDeleteViewSet(
    ModelViewSetBase,
    List,
    Retrieve,
    Destroy,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to delete and view ONLY!"""

    pass



class ModelRetrieveUpdateViewSet(
    ModelViewSetBase,
    Retrieve,
    Update,
    viewsets.GenericViewSet,
):
    """ Use for models that you wish to update and view ONLY!"""

    pass



class ReadOnlyModelViewSet(
    ModelViewSetBase,
    Retrieve,
    List,
    viewsets.GenericViewSet,
):


    pass



class ReadOnlyListModelViewSet(
    ModelViewSetBase,
    List,
    viewsets.GenericViewSet,
):


    pass



class AuthUserReadOnlyModelViewSet(
    ReadOnlyModelViewSet
):
    """Authenticated User Read-Only Viewset

    Use this class if the model only requires that the user be authenticated
    to obtain view permission.

    Args:
        ReadOnlyModelViewSet (class): Read-Only base class
    """

    permission_classes = [
        IsAuthenticated,
    ]


class IndexViewset(
    ModelViewSetBase,
):

    permission_classes = [
        IsAuthenticated,
    ]


class StaticPageNumbering(
    pagination.PageNumberPagination
):
    """Enforce Page Numbering

    Enfore results per page min/max to static value that cant be changed.
    """

    page_size = 20

    max_page_size = 20



class PublicReadOnlyViewSet(
    ReadOnlyListModelViewSet
):
    """Public Viewable ViewSet

    User does not need to be authenticated. This viewset is intended to be
    inherited by viewsets that are intended to be consumed by unauthenticated
    public users.

    URL **must** be prefixed with `public`

    Args:
        ReadOnlyModelViewSet (ViewSet): Common Read-Only Viewset
    """

    pagination_class = StaticPageNumbering

    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    metadata_class = JSONAPIMetadata
