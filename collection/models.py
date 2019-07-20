from django.db import models
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from users.models import User
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True, verbose_name=_('location'))
    registration_number = models.CharField(max_length=15, unique=True, verbose_name=_('registration_number'))
    model = models.CharField(max_length=20, blank=True, verbose_name=_('model'))
    users = models.ManyToManyField(to=User, blank=True, related_name='vehicle', verbose_name=_('users'))

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def __str__(self):
        return self.registration_number + " - " + self.model


class Item(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return self.name


class CollectionPoint(models.Model):
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True, verbose_name=_('location'))
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    area = models.ForeignKey(to=Area, on_delete=None, null=True, blank=True, related_name='collection_point',
                             verbose_name=_('area'))

    class Meta:
        verbose_name = _('CollectionPoint')
        verbose_name_plural = _('CollectionPoints')

    def __str__(self):
        return self.name


class Pickup(models.Model):
    collection_point = models.ForeignKey(to=CollectionPoint, on_delete=None, null=True, related_name='pickup',
                                         verbose_name=_('collection_point'))
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None, related_name='pickup', null=True, verbose_name=_('vehicle'))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_('timestamp'))
    image = models.FileField(blank=True, null=True, verbose_name=_('image'))
    items = models.ManyToManyField(to=Item, verbose_name=_('items'))
    users = models.ManyToManyField(to=User, blank=True, verbose_name=_('users'))
    route = models.TextField(blank=True, verbose_name=_('route'))

    class Meta:
        verbose_name = _('Pickup')
        verbose_name_plural = _('Pickups')

    def __str__(self):
        return str(self.timestamp)
