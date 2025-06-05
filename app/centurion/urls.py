"""
URL configuration for itsm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_centurion.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import include, path, re_path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls, name='_administration'),

    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name="password_change.html.j2"), name="change_password"),

    path("account/", include("django.contrib.auth.urls")),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


]


if settings.SSO_ENABLED:

    urlpatterns += [
        path('sso/', include('social_django.urls', namespace='social'))
    ]


if settings.API_ENABLED:

    urlpatterns += [

        path("api/", include("api.urls", namespace = 'v1')),
        path('api/schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
        path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

        path("api/v2/", include("api.urls_v2", namespace = 'v2')),

    ]


    urlpatterns += [
        path('api/v2/auth/', include('rest_framework.urls')),
    ]



if settings.DEBUG:

    urlpatterns += [

        path("__debug__/", include("debug_toolbar.urls"), name='_debug'),
    ]
