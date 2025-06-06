from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import include, path, re_path



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

        path("api/v2/", include("api.urls_v2", namespace = 'v2')),

    ]


    urlpatterns += [
        path('api/v2/auth/', include('rest_framework.urls')),
    ]



if settings.DEBUG:

    urlpatterns += [

        path("__debug__/", include("debug_toolbar.urls"), name='_debug'),
    ]
