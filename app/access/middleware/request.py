from django.utils.deprecation import MiddlewareMixin

from settings.models.app_settings import AppSettings


class RequestTenancy(MiddlewareMixin):
    """Access Middleware

    Serves the purpose of adding the users tenancy details to rhe request
    object.
    """


    def process_request(self, request):

        request.app_settings = AppSettings.objects.select_related('global_organization').filter(
            owner_organization = None
        )[0]
