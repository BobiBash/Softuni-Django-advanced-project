from datetime import datetime, timedelta
from time import strftime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
import json

from django.views.generic import CreateView, TemplateView, ListView

from appointments.models import AppointmentSlot, Appointment
from pets.models import Pet


# Create your views here.
class VetScheduleView(LoginRequiredMixin, View):
    def get(self, request, slug):
        slots = AppointmentSlot.objects.filter(
            vet_id=request.user.vet_profile
        ).values('date', 'time')

        return render(request, 'appointments/manage_schedule.html', {
        'slots': json.dumps(list(slots), default=str),
        'vet_slug': request.user.vet_profile.slug,
    })

    def post(self, request, slug):
        vet_id = request.user.vet_profile.id
        print(vet_id)
        date = request.POST.get('date')
        times = request.POST.getlist('time')
        AppointmentSlot.objects.filter(vet_id=vet_id, date=date).delete()

        for time in times:
            AppointmentSlot.objects.get_or_create(
                date=date,
                time=time,
                vet_id=vet_id
            )
        return redirect('vet-schedule', slug)

class UserMakeAppointMentView(LoginRequiredMixin, View):
    def post(self, request, slug):
        owner_id = request.user.pk
        slot_id = request.POST.get('slot')
        pet_id = request.POST.get('pet')

        Appointment.objects.create(owner_id=owner_id, slot_id=slot_id, pet_id=pet_id)

        return redirect('vets-list')


class UserAppointmentsView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'accounts/user_appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user)