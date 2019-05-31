from rest_framework import serializers
from .models import Vehicle, CollectionPoint, Item, Area


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'registration_number', 'model', 'location', 'users']


class CollectionPointSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = CollectionPoint
        fields = ['items', 'name', 'address']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['name', 'description']
