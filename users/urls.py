from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, base_name='profile')
router.register(r'', UserViewSet, base_name='user')
urlpatterns = router.urls
