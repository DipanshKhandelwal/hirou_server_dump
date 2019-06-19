from django.db import models
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from users.models import User


class Vehicle(models.Model):
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True)
    registration_number = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=20, blank=True)
    users = models.ManyToManyField(to=User, blank=True, related_name='vehicle')

    def __str__(self):
        return self.registration_number + " - " + self.model


class Item(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CollectionPoint(models.Model):
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True)  # remove null=True
    name = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=100, blank=True)
    area = models.ForeignKey(to=Area, on_delete=None, null=True, blank=True, related_name='collection_point')  # remove null=True

    def __str__(self):
        return self.name


class Pickup(models.Model):
    collection_point = models.ForeignKey(to=CollectionPoint, on_delete=None, null=True, related_name='pickup')  # remove null=True
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None, related_name='pickup', null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.FileField(blank=True, null=True)
    items = models.ManyToManyField(to=Item)
    users = models.ManyToManyField(to=User, blank=True)
    route = models.TextField(blank=True)

    def __str__(self):
        return str(self.timestamp)
