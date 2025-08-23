from django.apps import apps
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from centurion_feature_flag.urls.routers import DefaultRouter

from api.viewsets import (
    index as v2
)

from centurion.viewsets.base import (
    index as base_index_v2,
    content_type as content_type_v2,
    permisson,
    user
)

from core.viewsets import (
    audit_history,
    centurion_model_notes,
)

app_name = "API"


history_type_names = ''
history_app_labels = ''
notes_type_names = ''
notes_app_labels = ''

for model in apps.get_models():

    if getattr(model, '_audit_enabled', False):

        history_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in history_app_labels:

            history_app_labels += model._meta.app_label + '|'


    if getattr(model, '_notes_enabled', False):

        notes_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in notes_app_labels:

            notes_app_labels += model._meta.app_label + '|'


history_app_labels = str(history_app_labels)[:-1]
history_type_names = str(history_type_names)[:-1]

notes_app_labels = str(notes_app_labels)[:-1]
notes_type_names = str(notes_type_names)[:-1]

router = DefaultRouter(trailing_slash=False)


router.register('', v2.Index, basename='_api_v2_home')


router.register('/base', base_index_v2.Index, basename='_api_v2_base_home')
router.register('/base/content_type', content_type_v2.ViewSet, basename='_api_v2_content_type')
router.register('/base/permission', permission.ViewSet, basename='_api_permission')
router.register('/base/user', user.ViewSet, basename='_api_user')



router.register(
    prefix = f'/(?P<app_label>[{history_app_labels}]+)/(?P<model_name>[{history_type_names} \
        ]+)/(?P<model_id>[0-9]+)/history',
    viewset = audit_history.ViewSet,
    basename = '_api_centurionaudit_sub'
)

router.register(
    prefix = f'/(?P<app_label>[{notes_app_labels}]+)/(?P<model_name>[{notes_type_names} \
        ]+)/(?P<model_id>[0-9]+)/notes',
    viewset = centurion_model_notes.ViewSet,
    basename = '_api_centurionmodelnote_sub'
)


urlpatterns = [

    path('/schema', SpectacularAPIView.as_view(api_version='v2'), name='schema-v2',),
    path('/docs', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='_api_v2_docs'),

]

urlpatterns += router.urls

urlpatterns += [
    path(route = "/access", view = include("access.urls_api")),
    path(route = "/accounting", view = include("accounting.urls")),
    path(route = "/assistance", view = include("assistance.urls_api")),
    path(route = "/config_management", view = include("config_management.urls_api")),
    path(route = "/core", view = include("core.urls_api")),
    path(route = "/devops", view = include("devops.urls")),
    path(route = "/hr", view = include('human_resources.urls')),
    path(route = "/itam", view = include("itam.urls_api")),
    path(route = "/itim", view = include("itim.urls_api")),
    path(route = "/project_management", view = include("project_management.urls_api")),
    path(route = "/settings", view = include("settings.urls_api")),
    path(route = '/public', view = include('api.urls_public')),
]
