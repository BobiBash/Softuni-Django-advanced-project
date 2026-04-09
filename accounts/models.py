from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .choices import PawMedicUserType
from autoslug import AutoSlugField


# Create your models here.
class PawMedicUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True, null=True)
    role = models.CharField(max_length=20, choices=PawMedicUserType.choices, default=PawMedicUserType.OWNER)
    is_active = models.BooleanField(default=False)

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"


class EmailConfirmation(models.Model):
    user = models.OneToOneField(PawMedicUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class VetProfile(models.Model):
    user = models.OneToOneField(PawMedicUser, on_delete=models.CASCADE, related_name='vet_profile')
    favorite_vets = models.ManyToManyField(PawMedicUser, through="FavoriteVet", related_name='favorite_vets')
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='vet_photos/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='get_fullname', unique=True)

    def get_fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

class FavoriteVet(models.Model):
    owner = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE, related_name='fav_vet')
    vet = models.ForeignKey(VetProfile, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)