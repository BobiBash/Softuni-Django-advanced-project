from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from .choices import PawMedicUserType


# Create your models here.
class PawMedicUser(SimpleEmailConfirmationUserMixin, AbstractUser):
    email = models.EmailField(unique=True)

    phone = PhoneNumberField(unique=True, null=True)
    role = models.CharField(max_length=20, choices=PawMedicUserType.choices, default=PawMedicUserType.OWNER)
    is_active = models.BooleanField(default=False)


#class UserProfile(models.Model):
