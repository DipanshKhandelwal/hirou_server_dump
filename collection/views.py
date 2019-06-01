from rest_framework import viewsets
from .serializers import VehicleSerializer, CollectionPointSerializer, ItemSerializer, AreaSerializer, PickupSerializer
from .models import Vehicle, CollectionPoint, Item, Area, Pickup


class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle instances.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def perform_update(self, serializer):
        vehicle = self.get_object()
        users = list(vehicle.users.all())
        users = [str(x.id) for x in users]
        data_users = self.request.data.getlist('users')
        user_id = str(self.request.user.id)
        if data_users:
            if user_id in data_users:
                if user_id not in users:
                    users.append(user_id)
            else:
                if user_id in users:
                    users.remove(user_id)
        serializer.save(users=users)


class CollectionPointViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing collection point instances.
    """
    serializer_class = CollectionPointSerializer
    queryset = CollectionPoint.objects.all()


class ItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing item instances.
    """
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class AreaViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing collection area instances.
    """
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


class PickupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing collection area instances.
    """
    serializer_class = PickupSerializer
    queryset = Pickup.objects.all()

    def perform_create(self, serializer):
        vehicle = Vehicle.objects.filter(users=self.request.user).order_by('id')
        if vehicle:
            vehicle = vehicle[0]
            users = vehicle.users.all()
            serializer.save(users=users, vehicle=vehicle)
        else:
            serializer.save(users=[self.request.user])
