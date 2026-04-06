from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import PawMedicUser
from .choices import PawMedicUserType


@receiver(post_save, sender=PawMedicUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == PawMedicUserType.VET:
            group, _ = Group.objects.get_or_create(name="Vets")
        else:
            group, _ = Group.objects.get_or_create(name="Pet Owners")
        instance.groups.add(group)


@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    if sender.name != "accounts":
        return

    vets_group, _ = Group.objects.get_or_create(name="Vets")
    owners_group, _ = Group.objects.get_or_create(name="Pet Owners")

    def get_perm(codename, app_label, model):
        ct = ContentType.objects.get(app_label=app_label, model=model)
        return Permission.objects.get(codename=codename, content_type=ct)

    vets_group.permissions.set(
        [
            get_perm("change_vetprofile", "accounts", "vetprofile"),
            get_perm("change_appointmentslot", "appointments", "appointmentslot"),
            get_perm("add_forumpost", "forum", "forumpost"),
            get_perm("change_forumpost", "forum", "forumpost"),
            get_perm("delete_forumpost", "forum", "forumpost"),
            get_perm("add_comment", "forum", "comment"),
            get_perm("change_comment", "forum", "comment"),
            get_perm("delete_comment", "forum", "comment"),
            get_perm("add_tag", "forum", "tag"),
            get_perm("change_tag", "forum", "tag"),
            get_perm("delete_tag", "forum", "tag"),
            get_perm("add_service", "accounts", "service"),
            get_perm("change_service", "accounts", "service"),
            get_perm("delete_service", "accounts", "service"),
            get_perm("view_pet", "pets", "pet"),
        ]
    )

    owners_group.permissions.set(
        [
            get_perm("add_pet", "pets", "pet"),
            get_perm("view_pet", "pets", "pet"),
            get_perm("change_pet", "pets", "pet"),
            get_perm("delete_pet", "pets", "pet"),
            get_perm("add_forumpost", "forum", "forumpost"),
            get_perm("change_forumpost", "forum", "forumpost"),
            get_perm("delete_forumpost", "forum", "forumpost"),
            get_perm("add_comment", "forum", "comment"),
            get_perm("change_comment", "forum", "comment"),
            get_perm("delete_comment", "forum", "comment"),
            get_perm("add_appointment", "appointments", "appointment"),
            get_perm("view_appointment", "appointments", "appointment"),
        ]
    )
