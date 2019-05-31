from .views import VehicleViewSet, CollectionPointViewSet, ItemViewSet, AreaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicle', VehicleViewSet, base_name='vehicle')
router.register(r'collection_point', CollectionPointViewSet, base_name='collection_point')
router.register(r'item', ItemViewSet, base_name='item')
router.register(r'area', AreaViewSet, base_name='area')

urlpatterns = router.urls
