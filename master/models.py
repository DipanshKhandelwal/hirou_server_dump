from django.db import models
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from users.models import User
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True, verbose_name=_('location'))
    registration_number = models.CharField(max_length=15, unique=True, verbose_name=_('registration_number'))
    model = models.CharField(max_length=20, blank=True, verbose_name=_('model'))
    # users = models.ManyToManyField(to=User, blank=True, related_name='vehicle', verbose_name=_('users'))

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')

    def __str__(self):
        return self.registration_number + " - " + self.model


class Customer(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __str__(self):
        return self.name


class Garbage(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('Garbage')
        verbose_name_plural = _('Garbages')

    def __str__(self):
        return self.name


class BaseRoute(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))
    customer = models.ForeignKey(to=Customer, verbose_name=_('customer'), on_delete=models.SET_NULL, null=True)
    garbage = models.ManyToManyField(to=Garbage, verbose_name=_('garbage'), related_name='route', blank=True)

    class Meta:
        verbose_name = _('BaseRoute')
        verbose_name_plural = _('BaseRoutes')

    def __str__(self):
        return self.name


class CollectionPoint(models.Model):
    route = models.ForeignKey(to=BaseRoute, verbose_name=_('route'), on_delete=models.SET_NULL, null=True, related_name='collection_point')
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name=_('location'))
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    sequence = models.IntegerField(verbose_name=_('sequence'), null=True)
    image = models.FileField(verbose_name=_('image'), blank=True, null=True)

    class Meta:
        verbose_name = _('CollectionPoint')
        verbose_name_plural = _('CollectionPoints')

    def __str__(self):
        return self.name


class Collection(models.Model):
    collection_point = models.ForeignKey(to=CollectionPoint, on_delete=models.SET_NULL, null=True, related_name='collection',
                                         verbose_name=_('collection_point'))
    available = models.BooleanField()

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

    def __str__(self):
        return str(self.timestamp)


class TaskRoute(models.Model):
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))
    customer = models.ForeignKey(to=Customer, verbose_name=_('customer'), on_delete=models.SET_NULL, null=True)
    garbage = models.ManyToManyField(to=Garbage, verbose_name=_('garbage'), blank=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name


class TaskCollectionPoint(models.Model):
    route = models.ForeignKey(to=TaskRoute, verbose_name=_('route'), on_delete=models.SET_NULL, null=True, related_name='task_collection_point')
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name=_('location'))
    name = models.CharField(max_length=20, verbose_name=_('name'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    sequence = models.IntegerField(verbose_name=_('sequence'))
    image = models.FileField(verbose_name=_('image'), blank=True, null=True)

    class Meta:
        verbose_name = _('TaskCollectionPoint')
        verbose_name_plural = _('TaskCollectionPoints')

    def __str__(self):
        return self.name


class TaskCollection(models.Model):
    collection_point = models.ForeignKey(to=TaskCollectionPoint, verbose_name=_('collection_point'), on_delete=models.SET_NULL, null=True, related_name='task_collection')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_('timestamp'))
    complete = models.BooleanField()
    amount = models.IntegerField(default=0)
    image = models.FileField(blank=True, null=True, verbose_name=_('image'))
    users = models.ForeignKey(to=User, blank=True, verbose_name=_('users'), on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None, related_name='collection', null=True,
                                verbose_name=_('vehicle'))
    garbage = models.ForeignKey(to=Garbage, verbose_name=_('garbage'), on_delete=models.SET_NULL, null=True)
    available = models.BooleanField()
