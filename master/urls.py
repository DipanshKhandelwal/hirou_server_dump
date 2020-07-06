from .views import VehicleViewSet, CollectionPointViewSet, GarbageViewSet, ReportTypeViewSet, CustomerViewSet, BaseRouteViewSet, TaskRouteViewSet, TaskCollectionPointViewSet, TaskCollectionViewSet, TaskReportViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'vehicle', VehicleViewSet, base_name='vehicle')
router.register(r'collection_point', CollectionPointViewSet, base_name='collection_point')
router.register(r'garbage', GarbageViewSet, base_name='garbage')
router.register(r'report_type', ReportTypeViewSet, base_name='report_type')
router.register(r'customer', CustomerViewSet, base_name='customer')
router.register(r'base_route', BaseRouteViewSet, base_name='base_route')
#
router.register(r'task_route', TaskRouteViewSet, base_name='task_route')
router.register(r'task_collection_point', TaskCollectionPointViewSet, base_name='task_collection_point')
router.register(r'task_collection', TaskCollectionViewSet, base_name='task_collection')
router.register(r'task_report', TaskReportViewSet, base_name='task_report')


urlpatterns = router.urls
