from assistance.viewsets import (
    index as assistance_index_v2,
    knowledge_base as knowledge_base_v2,
    model_knowledge_base_article,
    request as request_ticket_v2,
)

from centurion_feature_flag.urls.routers import DefaultRouter



# app_name = "assistance"


router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix = '', viewset = assistance_index_v2.Index,
    basename = '_api_v2_assistance_home'
)
router.register(
    prefix = '/knowledge_base', viewset = knowledge_base_v2.ViewSet,
    basename = '_api_knowledgebase'
)
router.register(
    prefix = '/(?P<model>.+)/(?P<model_pk>[0-9]+)/knowledge_base',
    viewset = model_knowledge_base_article.ViewSet,
    basename = '_api_v2_model_kb'
)
router.register(
    prefix = '/ticket/request', viewset = request_ticket_v2.ViewSet,
    basename = '_api_v2_ticket_request'
)

urlpatterns = router.urls
