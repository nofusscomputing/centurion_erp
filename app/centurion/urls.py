import os

import prometheus_client

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.views.static import serve
from django.urls import include, path, re_path


from rest_framework import urls



urlpatterns = [
    path('admin/', admin.site.urls, name='_administration'),

    path('account/password_change', auth_views.PasswordChangeView.as_view(template_name="password_change.html.j2"), name="change_password"),

    path("account", include("django.contrib.auth.urls")),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


]


if settings.SSO_ENABLED:

    urlpatterns += [
        path('sso/', include('social_django.urls', namespace='social'))
    ]


if settings.API_ENABLED:

    urlpatterns += [

        path("api", include("api.urls", namespace = 'v1')),

        path("api/v2", include("api.urls_v2", namespace = 'v2')),

    ]


    urlpatterns += [
        path('api/v2/auth/login', auth_views.LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
        path('api/v2/auth/logout', auth_views.LogoutView.as_view(), name='logout'),
    ]



if settings.DEBUG:

    urlpatterns += [

        path("__debug__/", include("debug_toolbar.urls"), name='_debug'),
    ]

if settings.METRICS_ENABLED:

    def ExportToDjangoView(request):
        """Re-Write of upstream

        Required so that the prometheus python client global registry is used.

        If upstream (django-prometheus) implements this change, this fn can be
        removed and the django-prometheus url path used again.

        see: https://github.com/django-commons/django-prometheus/blob/d63a6d8803d5d88e4939788192edbebb2de354f0/django_prometheus/exports.py#L111-L122
        see: https://github.com/nofusscomputing/centurion_erp/issues/1156
        see: https://github.com/nofusscomputing/centurion_erp/issues/1162
        """

        metrics_page = prometheus_client.generate_latest(prometheus_client.REGISTRY)

        return HttpResponse(metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST)


    urlpatterns += [
        path(route = "metrics", view = ExportToDjangoView, name = "prometheus-django-metrics"),
    ]
