from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name=_('phone_number'))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name=_('gender'))
    date_of_birth = models.DateTimeField(blank=True, null=True, verbose_name=_('date_of_birth'))
    bio = models.CharField(max_length=200, blank=True, verbose_name=_('bio'))
    image = models.FileField(blank=True, null=True, verbose_name=_('image'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.user.username
