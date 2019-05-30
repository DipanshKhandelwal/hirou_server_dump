from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from collection.models import Vehicle


class User(AbstractUser):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    dob = models.DateTimeField(blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True)
    image = models.FileField(blank=True, null=True)
    vehicle = models.ForeignKey(to=Vehicle, on_delete=None, null=True, blank=True)

    def __str__(self):
        return self.user.username
