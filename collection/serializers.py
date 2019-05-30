from rest_framework import serializers
from .models import Vehicle, CollectionPoint


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'model', 'location']


class CollectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionPoint
        fields = ['items', 'name', 'address']
