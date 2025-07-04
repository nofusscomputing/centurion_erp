from django.core.exceptions import (    # pylint: disable=W0611:unused-import
    ObjectDoesNotExist
)

from django.http import Http404    # pylint: disable=W0611:unused-import

from rest_framework import exceptions, status
from rest_framework.exceptions import (    # pylint: disable=W0611:unused-import
    MethodNotAllowed,
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
    ValidationError,
)

class MissingAttribute(Exception):
    """ An attribute is missing"""

    pass

class APIError(
    exceptions.APIException
):

    status_code = status.HTTP_400_BAD_REQUEST

    default_detail = 'An unknown ERROR occured'

    default_code = 'unknown_error'


class NotModified(
    exceptions.APIException
):

    status_code = status.HTTP_304_NOT_MODIFIED

    default_detail = ''

    default_code = 'not_modified'