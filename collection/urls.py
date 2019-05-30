from .views import VehicleViewSet, CollectionPointViewSet, ItemViewSet, AreaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicles', VehicleViewSet, base_name='vehicles')
router.register(r'collection_points', CollectionPointViewSet, base_name='collection_points')
router.register(r'items', ItemViewSet, base_name='items')
router.register(r'areas', AreaViewSet, base_name='areas')

urlpatterns = router.urls
