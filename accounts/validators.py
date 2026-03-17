import re

from .models import PawMedicUser
from django.core.exceptions import ValidationError


def validate_password_strength(value):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit."
        )

def validate_username_taken(value):
    if PawMedicUser.objects.filter(username=value).exists():
        raise ValidationError("Username is already taken.")

