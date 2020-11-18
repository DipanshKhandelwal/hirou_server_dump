import requests
from django.db import models
from django.utils import timezone
from location_field.models.plain import PlainLocationField
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    name = models.CharField(max_length=20, verbose_name=_('name'))
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


class ReportType(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('ReportType')
        verbose_name_plural = _('ReportTypes')

    def __str__(self):
        return self.name


class BaseRoute(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('name'))
    customer = models.ForeignKey(to=Customer, verbose_name=_('customer'), on_delete=models.SET_NULL, null=True, related_name='route')
    garbage = models.ManyToManyField(to=Garbage, verbose_name=_('garbage'), related_name='route', blank=True)

    class Meta:
        verbose_name = _('BaseRoute')
        verbose_name_plural = _('BaseRoutes')

    def __str__(self):
        return self.name


class CollectionPoint(models.Model):
    route = models.ForeignKey(to=BaseRoute, verbose_name=_('route'), on_delete=models.CASCADE, null=True, related_name='collection_point')
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name=_('location'))
    name = models.CharField(max_length=20, verbose_name=_('name'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'), default="")
    memo = models.CharField(max_length=100, blank=True, verbose_name=_('memo'), default="")
    sequence = models.IntegerField(verbose_name=_('sequence'), null=True)
    image = models.FileField(verbose_name=_('image'), blank=True, null=True, upload_to='collection_points')

    class Meta:
        verbose_name = _('CollectionPoint')
        verbose_name_plural = _('CollectionPoints')

    def __str__(self):
        return self.name


class TaskRoute(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=30, verbose_name=_('name'))
    customer = models.ForeignKey(to=Customer, verbose_name=_('customer'), on_delete=models.SET_NULL, null=True, related_name='task_route')
    garbage = models.ManyToManyField(to=Garbage, verbose_name=_('garbage'), blank=True, related_name='task_route',)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=models.SET_NULL, related_name='task_route', null=True, verbose_name=_('vehicle'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = timezone.now()
        return super(TaskRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name


class TaskCollectionPoint(models.Model):
    route = models.ForeignKey(to=TaskRoute, verbose_name=_('route'), on_delete=models.CASCADE, null=True, related_name='task_collection_point')
    location = PlainLocationField(based_fields=['city'], zoom=7, verbose_name=_('location'))
    name = models.CharField(max_length=20, verbose_name=_('name'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'), default="")
    memo = models.CharField(max_length=100, blank=True, verbose_name=_('memo'), default="")
    sequence = models.IntegerField(verbose_name=_('sequence'))
    image = models.FileField(verbose_name=_('image'), blank=True, null=True)

    class Meta:
        verbose_name = _('TaskCollectionPoint')
        verbose_name_plural = _('TaskCollectionPoints')

    def __str__(self):
        return self.name


class TaskCollection(models.Model):
    collection_point = models.ForeignKey(to=TaskCollectionPoint, verbose_name=_('collection_point'), on_delete=models.CASCADE, null=True, related_name='task_collection')
    timestamp = models.DateTimeField(default=None, verbose_name=_('timestamp'), null=True)
    complete = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    image = models.FileField(blank=True, null=True, verbose_name=_('image'))
    users = models.ForeignKey(to=User, blank=True, verbose_name=_('users'), on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None, related_name='collection', null=True,
                                verbose_name=_('vehicle'))
    garbage = models.ForeignKey(to=Garbage, verbose_name=_('garbage'), on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('TaskCollection')
        verbose_name_plural = _('TaskCollections')

    def __str__(self):
        return self.collection_point.name + str(self.collection_point.sequence) + self.garbage.name


class TaskReport(models.Model):
    route = models.ForeignKey(to=TaskRoute, verbose_name=_('route'), on_delete=models.SET_NULL, null=True, related_name='report')
    task_collection_point = models.ForeignKey(to=TaskCollectionPoint, verbose_name=_('task_collection_point'), on_delete=models.SET_NULL, null=True, related_name='report')
    report_type = models.ForeignKey(to=ReportType, verbose_name=_('report_type'), on_delete=models.SET_NULL, null=True, related_name='report')
    image = models.FileField(verbose_name=_('image'), blank=True, null=True, upload_to='reports')
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), null=True)
    description = models.CharField(max_length=200, blank=True, verbose_name=_('description'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        return super(TaskReport, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('TaskReport')
        verbose_name_plural = _('TaskReports')

    def __str__(self):
        return str(self.timestamp)


def send_chatwork_notification(message, read):
    payload = {"body": message, "self_unread": read}
    headers = {'X-ChatWorkToken': '36df5b65d2584e27e28b3b3e16609fdd'}
    requests.post("https://api.chatwork.com/v2/rooms/200390378/messages", data=payload, headers=headers)


@receiver(post_save, sender=TaskReport, dispatch_uid="task_report_saved")
def task_report_saved(sender, instance, created, **kwargs):
    status = ""
    if created:
        status = "Report Created : "
    else:
        status = "Report Updated : "

    date = "\nDate :" + instance.timestamp.ctime()
    base_route_name = "\nTask Route : " + instance.route.name
    collection_point_name = "\nCollection Point : " + instance.task_collection_point.name
    report_type = "\nReport Type : " + instance.report_type.name
    description = "\nDescription : " + instance.description

    message = status + date + base_route_name + collection_point_name + report_type + description
    send_chatwork_notification(message, 1)


class TaskAmount(models.Model):
    route = models.ForeignKey(to=TaskRoute, verbose_name=_('route'), on_delete=models.SET_NULL, null=True, related_name='amount')
    garbage = models.ForeignKey(to=Garbage, verbose_name=_('garbage'), on_delete=models.SET_NULL, null=True, related_name='amount')
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, verbose_name=_('user'), on_delete=models.SET_NULL, null=True, related_name='amount')
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        return super(TaskAmount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('TaskAmount')
        verbose_name_plural = _('TaskAmounts')

    def __str__(self):
        return self.route.name + self.garbage.name + str(self.amount)
