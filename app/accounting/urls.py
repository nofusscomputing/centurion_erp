from django.apps import apps

from centurion_feature_flag.urls.routers import APIRootView, DefaultRouter

from accounting.viewsets import (
    asset,
    asset_notes,
)



class RootView(APIRootView):

    def get_view_name(self):

        return 'Accounting'



app_name = "accounting"

router = DefaultRouter(trailing_slash=False)

router.APIRootView = RootView


asset_type_names = ''


for model in apps.get_models():

    if issubclass(model, asset.AssetBase):
        
        if model._meta.sub_model_type == 'asset':
            continue

        asset_type_names += model._meta.sub_model_type + '|'



asset_type_names = str(asset_type_names)[:-1]

if not asset_type_names:
    asset_type_names = 'none'

router.register('asset/(?P<model_id>[0-9]+)/notes', asset_notes.ViewSet, feature_flag = '2025-00004', basename='_api_v2_asset_note')

router.register(f'asset/(?P<asset_model>[{asset_type_names}]+)?', asset.ViewSet, feature_flag = '2025-00004', basename='_api_v2_asset_sub')
router.register('asset', asset.NoDocsViewSet, feature_flag = '2025-00004', basename='_api_v2_asset')

urlpatterns = router.urls
