from rest_framework import viewsets
from .serializers import VehicleSerializer, CollectionPointSerializer, ItemSerializer, AreaSerializer, PickupSerializer
from .models import Vehicle, CollectionPoint, Item, Area, Pickup


class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle instances.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()


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
