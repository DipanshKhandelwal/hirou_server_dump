from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .serializers import VehicleSerializer, CollectionPointSerializer, GarbageSerializer, CustomerSerializer, BaseRouteSerializer, BaseRouteListSerializer, TaskRouteSerializer, TaskRouteListSerializer, TaskCollectionPointSerializer, TaskCollectionSerializer, ReportTypeSerializer, TaskReportSerializer, TaskReportListSerializer, TaskAmountSerializer, TaskAmountListSerializer
from .models import Vehicle, CollectionPoint, Garbage, ReportType, Customer, BaseRoute, TaskRoute, TaskCollectionPoint, TaskCollection, TaskReport, TaskAmount
from rest_framework.response import Response
from django.contrib.auth.models import User

from master.consumers.helpers import send_update_to_socket, get_channel_group_name
from .consumers.constants import SocketEventTypes, SocketChannels, SocketSubEventTypes


class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle instances.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    # def perform_update(self, serializer):
    #     vehicle = self.get_object()
    #     users = list(vehicle.users.all())
    #     users = [str(x.id) for x in users]
    #     data_users = self.request.data.get('users')
    #     user_id = str(self.request.user.id)
    #     if data_users:
    #         if int(user_id) in data_users:
    #             if user_id not in users:
    #                 users.append(user_id)
    #         else:
    #             if user_id in users:
    #                 users.remove(user_id)
    #     serializer.save(users=users)


class CollectionPointViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing collection point instances.
    """
    serializer_class = CollectionPointSerializer
    queryset = CollectionPoint.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            base_route_id = self.request.data["route"]
            route = BaseRoute.objects.get(id=base_route_id)
            collection_points = route.collection_point.all()
            if len(collection_points) > 0:
                last_cp = max(collection_points, key=lambda x: int(x.sequence))
                serializer.save(sequence=last_cp.sequence+1)
            else:
                serializer.save(sequence=1)

            data = BaseRouteListSerializer(route).data

            channel = get_channel_group_name(SocketChannels.BASE_ROUTE, base_route_id)
            send_update_to_socket(SocketEventTypes.COLLECTION_POINT, SocketSubEventTypes.CREATE, channel, data)

    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user)
        base_route = instance.route

        data = BaseRouteListSerializer(base_route).data

        channel = get_channel_group_name(SocketChannels.BASE_ROUTE, base_route.id)
        send_update_to_socket(SocketEventTypes.COLLECTION_POINT, SocketSubEventTypes.UPDATE, channel, data)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        base_route = instance.route
        collection_points = base_route.collection_point.all()
        for i, e in enumerate(sorted(collection_points, key=lambda x: x.sequence)):
            e.sequence = i+1
            e.save()

        data = BaseRouteListSerializer(base_route).data

        channel = get_channel_group_name(SocketChannels.BASE_ROUTE, base_route.id)
        send_update_to_socket(SocketEventTypes.COLLECTION_POINT, SocketSubEventTypes.DELETE, channel, data)


class GarbageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing garbage instances.
    """
    serializer_class = GarbageSerializer
    queryset = Garbage.objects.all()


class ReportTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing report type instances.
    """
    serializer_class = ReportTypeSerializer
    queryset = ReportType.objects.all()


class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class BaseRouteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing base route instances.
    """
    # serializer_class = BaseRouteSerializer
    queryset = BaseRoute.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseRouteListSerializer

        if self.action == 'retrieve':
            return BaseRouteListSerializer

        return BaseRouteSerializer
    
    @action(detail=True, methods=['post'])
    def copy(self, request, pk=None):
        base_route = self.get_object()

        new_base_route = BaseRoute(name=base_route.name + ' のコピー', customer = base_route.customer)
        new_base_route.save()

        garbages = base_route.garbage.all()
        new_base_route.garbage.add(*garbages)

        collection_points = base_route.collection_point.all()

        for cp in collection_points:
            new_collection_point = CollectionPoint()
            new_collection_point.location = cp.location
            new_collection_point.route = new_base_route
            new_collection_point.name = cp.name
            new_collection_point.address = cp.address
            new_collection_point.memo = cp.memo
            new_collection_point.sequence = cp.sequence
            new_collection_point.image = cp.image
            new_collection_point.save()

        new_base_route.save()

        return Response(BaseRouteSerializer(new_base_route).data)

    @action(detail=True, methods=['patch', 'post'])
    def reorder_points(self, request, pk=None):
        base_route = self.get_object()
        points = self.request.data["points"]

        for i, e in enumerate(points):
            cp = CollectionPoint.objects.get(pk=e)
            cp.sequence = i+1
            cp.save()

        data = BaseRouteListSerializer(base_route).data

        channel = get_channel_group_name(SocketChannels.BASE_ROUTE, base_route.id)
        send_update_to_socket(SocketEventTypes.BASE_ROUTE, SocketSubEventTypes.REORDER, channel, data)

        return Response(BaseRouteListSerializer(base_route).data)


# 
class TaskRouteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task route instances.
    """
    # serializer_class = TaskRouteSerializer
    queryset = TaskRoute.objects.all()

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return TaskRouteListSerializer

    def get_serializer_class(self):
        type = self.request.query_params.get('type', None)

        if type and type == 'list':
            return TaskRouteListSerializer

        return TaskRouteSerializer

    def get_queryset(self):
        queryset = TaskRoute.objects.all()
        date = self.request.query_params.get('date', None)

        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def perform_create(self, serializer):
        base_route_id = self.request.data["id"]
        new_task_name = self.request.data["name"]
        route = BaseRoute.objects.get(id=base_route_id)
        new_task_route = TaskRoute(name=new_task_name)
        new_task_route.customer = route.customer
        new_task_route.base_route_name = route.name

        new_task_route.save()

        garbages = route.garbage.all()
        new_task_route.garbage.add(*garbages)

        collection_points = route.collection_point.all()

        for cp in collection_points:
            new_task_collection_point = TaskCollectionPoint()
            new_task_collection_point.location = cp.location
            new_task_collection_point.route = new_task_route
            new_task_collection_point.name = cp.name
            new_task_collection_point.address = cp.address
            new_task_collection_point.memo = cp.memo
            new_task_collection_point.sequence = cp.sequence
            new_task_collection_point.image = cp.image
            new_task_collection_point.save()

            for garbage in garbages:
                new_collection = TaskCollection()
                new_collection.collection_point = new_task_collection_point
                new_collection.garbage = garbage
                new_collection.save()
                new_task_collection_point.task_collection.add(new_collection)

            new_task_route.task_collection_point.add(new_task_collection_point)

        new_task_route.save()


class TaskCollectionPointViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task collection point instances.
    """
    serializer_class = TaskCollectionPointSerializer
    queryset = TaskCollectionPoint.objects.all()

    @action(detail=True, methods=['patch', 'post'])
    def bulk_complete(self, request, pk=None):
        task_c_p = self.get_object()
        complete = True
        for tc in task_c_p.task_collection.all():
            if not tc.complete:
                complete = False
                break

        for tc in task_c_p.task_collection.all():
            if not complete:
                tc.complete = True
                tc.timestamp = timezone.now()
                tc.available = False
            else:
                tc.complete = False
                tc.timestamp = None
                tc.amount = 0

            tc.save()

        data = TaskCollectionPointSerializer(task_c_p).data

        channel = get_channel_group_name(SocketChannels.TASK_ROUTE, task_c_p.route.id)
        send_update_to_socket(SocketEventTypes.TASK_COLLECTION_POINT, SocketSubEventTypes.BULK_COMPLETE, channel, data)

        return Response(TaskCollectionSerializer(task_c_p.task_collection.all(), many=True).data)


class TaskCollectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task collection instances.
    """
    serializer_class = TaskCollectionSerializer
    queryset = TaskCollection.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user)
        data = TaskCollectionPointSerializer(instance.collection_point).data

        channel = get_channel_group_name(SocketChannels.TASK_ROUTE, instance.collection_point.route.id)
        send_update_to_socket(SocketEventTypes.TASK_COLLECTION, SocketSubEventTypes.UPDATE, channel, data)


class TaskReportViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task report instances.
    """
    queryset = TaskReport.objects.all()

    def get_queryset(self):
        queryset = TaskReport.objects.all()
        task_route = self.request.query_params.get('task_route', None)

        if task_route:
            queryset = queryset.filter(route=task_route)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskReportListSerializer

        return TaskReportSerializer


class TaskAmountViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing task amount instances.
    """
    serializer_class = TaskAmountSerializer
    queryset = TaskAmount.objects.all()

    def perform_create(self, serializer):
        task_amount = serializer.save()

        if self.request.user.id:
            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
            task_amount.user = user
            task_amount.save()

    def perform_update(self, serializer):
        try:
            user_id = self.request.user.id
            serializer.is_valid(raise_exception=True)
            if user_id:
                user = User.objects.get(id=user_id)
                serializer.save(user=user)
            else:
                serializer.save()
        except ValidationError:
            return Response({"errors": (serializer.errors,)},
                            status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = TaskAmount.objects.all()
        task_route = self.request.query_params.get('task_route', None)

        if task_route:
            queryset = queryset.filter(route=task_route)

        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TaskAmountListSerializer

        return TaskAmountSerializer
