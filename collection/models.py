from django.db import models
from users.models import User
from django.utils import timezone


class Vehicle(models.Model):
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    registration_number = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.registration_number + " - " + self.model


class Area(models.Model):
    description = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Pickup(models.Model):
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None)
    users = models.ManyToManyField(to=User)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.FileField(blank=True, null=True)
    area = models.ForeignKey(to=Area, on_delete=None, null=True)

    def __str__(self):
        return str(self.timestamp)


class Item(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class CollectionPoint(models.Model):
    items = models.ManyToManyField(to=Item)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
