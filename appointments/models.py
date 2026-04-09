from django.db import models

from accounts.models import VetProfile, PawMedicUser
from pets.models import Pet


# Create your models here.
class AppointmentSlot(models.Model):
    vet = models.ForeignKey(VetProfile, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    date_and_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

class Appointment(models.Model):
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE, related_name='slots')
    vet = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE, related_name='vets')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='pet')
