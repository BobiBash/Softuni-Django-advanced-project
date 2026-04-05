from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import PawMedicUser
from .choices import PawMedicUserType

@receiver(post_save, sender=PawMedicUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == PawMedicUserType.VET:
            group, _ = Group.objects.get(name='Vets')
        else:
            group, _ = Group.objects.get(name='Pet Owners')
        instance.groups.add(group)