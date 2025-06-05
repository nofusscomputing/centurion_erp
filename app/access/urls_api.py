from django.apps import apps

from centurion_feature_flag.urls.routers import DefaultRouter

from access.viewsets import (
    entity,
    index as access_v2,
    organization as organization_v2,
    role,
    team as team_v2,
    team_user as team_user_v2
)

entity_type_names = ''
history_type_names = ''
history_app_labels = ''
ticket_type_names = ''
ticket_comment_names = ''

for model in apps.get_models():

    if issubclass(model, entity.Entity):

        entity_type_names += model._meta.sub_model_type + '|'


entity_type_names = str(entity_type_names)[:-1]


# app_name = "access"

router = DefaultRouter(trailing_slash=False)

router.register('', access_v2.Index, basename = '_api_v2_access_home')

router.register(
    prefix = '(?P<entity_model>[company]+)', viewset = entity.ViewSet,
    feature_flag = '2025-00008',basename = '_api_v2_company'
)

router.register(
    prefix=f'entity/(?P<entity_model>[{entity_type_names}]+)?', viewset = entity.ViewSet,
    feature_flag = '2025-00002', basename = '_api_v2_entity_sub'
)

router.register(
    prefix = 'entity', viewset = entity.NoDocsViewSet,
    feature_flag = '2025-00002', basename = '_api_v2_entity'
)

# router.register(
#     prefix = 'access/entity/(?P<model_id>[0-9]+)/notes', viewset = entity_notes.ViewSet,
#     feature_flag = '2025-00002', basename = '_api_v2_entity_note'
# )

router.register(
    prefix = 'tenant', viewset = organization_v2.ViewSet,
    basename = '_api_v2_organization'
)

# router.register(
#     prefix = 'tenant/(?P<model_id>[0-9]+)/notes', viewset = organization_notes.ViewSet,
#     basename = '_api_v2_organization_note'
# )

router.register(
    prefix = 'tenant/(?P<organization_id>[0-9]+)/team', viewset = team_v2.ViewSet,
    basename = '_api_v2_organization_team'
)

# router.register(
#     prefix = 'tenant/(?P<organization_id>[0-9]+)/team/(?P<model_id>[0-9]+)/notes',
#     viewset = team_notes.ViewSet,
#     basename = '_api_v2_team_note'
# )

router.register(
    prefix = 'access/tenant/(?P<organization_id>[0-9]+)/team/(?P<team_id>[0-9]+)/user',
    viewset = team_user_v2.ViewSet,
    basename = '_api_v2_organization_team_user'
)

router.register(
    prefix = 'role', viewset = role.ViewSet,
    feature_flag = '2025-00003', basename = '_api_v2_role'
)

# router.register(
#     prefix = 'role/(?P<model_id>[0-9]+)/notes', viewset = role_notes.ViewSet,
#     feature_flag = '2025-00003', basename = '_api_v2_role_note'
# )

urlpatterns = router.urls
