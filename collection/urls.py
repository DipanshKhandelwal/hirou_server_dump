from .views import VehicleViewSet, CollectionPointViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicles', VehicleViewSet, base_name='vehicles')
router.register(r'collection_points', CollectionPointViewSet, base_name='collection_points')

urlpatterns = router.urls
