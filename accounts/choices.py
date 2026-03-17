from django.db import models

class PawMedicUserType(models.TextChoices):
    OWNER = 'OWNER', 'Owner'
    VET = 'VET', 'Veterinarian'