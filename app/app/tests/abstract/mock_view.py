
import django

from access.middleware.request import Tenancy
from access.models.tenant import Tenant as Organization

from settings.models.app_settings import AppSettings

User = django.contrib.auth.get_user_model()



class MockView:

    action: str = None

    app_settings: AppSettings = None

    kwargs: dict = {}

    request = None


    def __init__(self, user: User, model = None):

        app_settings = AppSettings.objects.select_related('global_organization').get(
            owner_organization = None
        )

        if model is not None:

            self.model = model

        self.request = MockRequest( user = user, app_settings = app_settings)



class MockRequest:

    tenancy: Tenancy = None

    user = None

    def __init__(self, user: User, app_settings):

        self.user = user

        self.app_settings = app_settings

        self.tenancy = Tenancy(
            user = user,
            app_settings = app_settings
        )
