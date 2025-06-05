from centurion_feature_flag.urls.routers import DefaultRouter

from itim.viewsets import (
    index as itim_v2,
    change,
    cluster as cluster_v2,
    incident,
    problem,
    service as service_v2,
    service_cluster,
)



# app_name = "itim"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = itim_v2.Index,
    basename = '_api_v2_itim_home'
)
router.register(
    prefix = 'ticket/change', viewset = change.ViewSet,
    basename = '_api_v2_ticket_change'
)
router.register(
    prefix = 'cluster', viewset = cluster_v2.ViewSet,
    basename = '_api_v2_cluster'
)
router.register(
    prefix = 'cluster/(?P<cluster_id>[0-9]+)/service', viewset = service_cluster.ViewSet,
    basename = '_api_v2_service_cluster'
)
router.register(
    prefix = 'ticket/incident', viewset = incident.ViewSet,
    basename = '_api_v2_ticket_incident'
)
router.register(
    prefix = 'ticket/problem', viewset = problem.ViewSet,
    basename = '_api_v2_ticket_problem'
)
router.register(
    prefix = 'service', viewset = service_v2.ViewSet,
    basename = '_api_v2_service'
)


urlpatterns = router.urls
