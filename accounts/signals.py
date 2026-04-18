from django.db.models.signals import post_migrate, post_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import PawMedicUser
from .choices import PawMedicUserType

@receiver(post_save, sender=PawMedicUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == PawMedicUserType.VET:
            vets_group = Group.objects.get(name="Vets")
            instance.groups.add(vets_group)
            print(f"Assigned user {instance.username} to 'Vets' group")
        elif instance.role == PawMedicUserType.OWNER:
            owners_group = Group.objects.get(name="Pet Owners")
            instance.groups.add(owners_group)
            print(f"Assigned user {instance.username} to 'Pet Owners' group")
