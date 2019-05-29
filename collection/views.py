from rest_framework import viewsets
from .serializers import VehicleSerializer
from .models import Vehicle


class VehicleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing vehicle instances.
    """
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
