from django.db import models

from accounts.models import PawMedicUser


class Pet(models.Model):
    owner = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    pet_photo = models.ImageField(null=True, blank=True)