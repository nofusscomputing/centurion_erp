# No Fuss Computing - Centurion ERP Feature Flag Client

This Django application serves the purpose of using feature flags as part of a Django applications development. You will require your own deployment of [Centurion ERP](https://nofusscomputing.com/projects/centurion_erp/) which is where the [feature flags](https://nofusscomputing.com/projects/centurion_erp/user/devops/feature_flags/) will be defined.

To setup the feature flagging the following will need to be added to your Django applications settings:

``` py
# settings.py

feature_flag = {
    'url': 'https://127.0.0.1:8002/api/v2/public/1/flags/2844',    # URL to your Centurion ERP instance
    'user_agent': 'My Django Application Name',                    # The name of your Django Application
    'cache_dir': str(BASE_DIR) + '/',                              # Directory name (with trailing slash `/`) where the cached flags will be stored
    'disable_downloading': False                                   # Prevent downloading feature flags
    'unique_id': 'unique ID for application',                      # Unique ID for this instance of your Django application
    'version': '1.0.0',                                            # The Version of Your Django Application
    'over_rides': []                                               # list(dict). Feature Flag over rides. use same format as API endpoint.
}    # Note: All key values are strings

```

!!! danger
    Failing to add the `feature_flag` dictionary to your Django Applications setting.py file will leave feature flagging **disabled**.


## Features

Within Django the following locations have the feature flagging available

- anywhere you can access the `request` object

- Django DRF Router(s)

- Django URLs

- Management command to fetch feature flag file

- Caching of flags


## Request Object

Any location within your django project where you can access the `request` object, you can use feature flagging. To enable this add the following to your middleware:

``` py

MIDDLEWARE = [
    ...
    'centurion_feature_flag.middleware.feature_flag.FeatureFlagMiddleware',
]

```

After the middleware has been added, property `feature_flag` is added to the request object.

Example usage within a view and/or Django DRF ViewSet:

``` py

class MyView:


    def get_queryset(self):

        if self.request.feature_flag['2025-00001']:

            # code to run if feature flag is enabled

```


## Django URLs

To enable feature flagging for urls, substitute `from django.urls import path, re_path` with `from centurion_feature_flag.urls.django import path, re_path`. Then optionally, whilst calling the `path` function include attribute `feature_flag` with a string value of the feature flag id. Once enabled if an attempt to navigate to the url is made and for a disabled feature flag, a `HTTP/404` will be returned.

``` py

# urls.py

from django.contrib import admin

from centurion_feature_flag.urls.django import (
    include,
    path,
    re_path
)

from my_app.views import home

urlpatterns = [
    path('', home.HomeView.as_view(), name='home', feature_flag = '2025-00001'),

    path('admin/', admin.site.urls, name='_administration'),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}, feature_flag = '2025-00003'),

    path("some-path/", include("my_app.urls"), feature_flag = '2025-00002'),

]

```

!!! tip
    module `centurion_feature_flag.urls.django` also contains function `include` from `django.urls` so there is no need to import `django.urls` for this function.

!!! note
    If you use feature flagging on the `path` function and its called with the `include` function as the view attribute, not all paths from the include function are available. As a consequence, sub-paths are unavailable. For example. The `some-path/` url can be navigated to whilst `some-path/sub-path/` can not be. This generally wont be an issue, although if you attempt to use the `reverse` function on the sub-path and the feature flag is disabled; the reverse function will raise an exception.


## DRF Router

Enabling feature flagging for Django DRF Routers is as simple as substituting `from rest_framework.routers import <router name>` with `from centurion_feature_flag.urls.routers import <router name>` then optionally updating the route register method with the feature flag to use. for example, using feature flag `2025-00001`

``` py

from centurion_feature_flag.urls.routers import DefaultRouter

from some_app.viewsets import my_viewset

router = DefaultRouter(trailing_slash=False)

router.register('my_viewset_path', my_viewset.ViewSet, feature_flag = '2025-00001', basename='_my_view_name')

urlpatterns = router.urls

```

!!! warning
    If a feature flag is updated any router that contains a feature flag that has been edited since Django was last restarted, will not be updated. To ensure that any router that uses feature flagging has the most up to date feature flag configuration. After downloading your feature flags, please restart your Django App.

!!! danger
    If the feature flags have not been downloaded and cached before your Django app is started. Any router that relies upon a feature flag will not be enabled. this is by design so that in the event you are unable to fetch the feature flags from your Centurion ERP instance, no feature will be unintentionally enabled.


## Management Command

The management command available is `feature_flag` with optional argument `--reload`. running this will download the available feature flags from the configured Centurion ERP Instance. To fetch the feature flags run command `python manage.py feature_flag --reload`.


!!! note
    Arg `--reload` only works within production. Which in this case is when Centurion ERP is deployed using one of our [docker containers](https://hub.docker.com/r/nofusscomputing/centurion-erp)


## Caching

The feature flags are saved to the local file system and updated every four hours.
