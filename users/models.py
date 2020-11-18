from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user_registration_number = models.CharField(max_length=40, blank=True, null=True, unique=True, verbose_name=_('user_registration_number'), default="")
    phone_number = models.CharField(max_length=17, blank=True, verbose_name=_('phone_number'), default="")
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name=_('gender'), default='M')
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('date_of_birth'))
    bio = models.CharField(max_length=200, blank=True, verbose_name=_('bio'), default="")
    image = models.FileField(blank=True, null=True, verbose_name=_('image'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.user.username
