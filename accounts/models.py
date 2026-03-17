from tkinter.constants import CASCADE

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .choices import PawMedicUserType


# Create your models here.
class PawMedicUser(AbstractUser):
    email = models.EmailField(unique=True)

    phone = PhoneNumberField(unique=True, null=True)
    role = models.CharField(max_length=20, choices=PawMedicUserType.choices, default=PawMedicUserType.OWNER)
    is_active = models.BooleanField(default=False)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(PawMedicUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

#class UserProfile(models.Model):
