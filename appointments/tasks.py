from celery import shared_task
from django.core.mail import send_mail
from PawMedic import settings

@shared_task
def send_appointment_notification(user_email, appointment_details):
    send_mail(
        subject='Your appointment details',
        message=f"""
        Your appointment has been booked:

        Date: {appointment_details['date']}
        Time: {appointment_details['time'].strftime('%H:%M')}
        Vet: {appointment_details['vet_name']}
        Pet: {appointment_details['pet_name']}
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )