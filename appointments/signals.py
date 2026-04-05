from django.core.mail import send_mail

from PawMedic import settings
from appointments.models import Appointment
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import send_appointment_notification



@receiver(post_save, sender=Appointment)
def notify_user_appointment_booked(sender, instance, created, **kwargs):
    if created:
        send_appointment_notification.delay(
            user_email=instance.vet.email,
            appointment_details={
                'date': instance.slot.date,
                'time': instance.slot.time,
                'vet_name': instance.vet.get_fullname(),
                'pet_name': instance.pet.name
            }
        )
