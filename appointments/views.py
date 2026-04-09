from datetime import datetime, timedelta
from time import strftime, strptime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views import View
import json

from django.views.generic import CreateView, TemplateView, ListView

from accounts.choices import PawMedicUserType
from appointments.models import AppointmentSlot, Appointment
from pets.models import Pet


# Create your views here.
class VetScheduleView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "appointments.change_appointmentslot"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != PawMedicUserType.VET:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, slug):
        slots = AppointmentSlot.objects.filter(vet_id=request.user.vet_profile).values(
            "date", "time"
        )

        return render(
            request,
            "appointments/manage_schedule.html",
            {
                "slots": json.dumps(list(slots), default=str),
                "vet_slug": request.user.vet_profile.slug,
            },
        )

    def post(self, request, slug):
        vet_id = request.user.vet_profile.id
        print(vet_id)
        date = request.POST.get("date")
        times = request.POST.getlist("time")
        AppointmentSlot.objects.filter(vet_id=vet_id, date=date).delete()

        for time in times:
            datetime_str = date + " " + time
            formatted_data = parse_datetime(datetime_str)
            formatted_data = timezone.make_aware(formatted_data)
            AppointmentSlot.objects.get_or_create(date=date, time=time, vet_id=vet_id, date_and_time=formatted_data)
        return redirect("vet-schedule", slug)


class UserMakeAppointMentView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = "appointments.add_appointment"

    def post(self, request, slug):
        owner_id = request.user.pk
        slot_id = request.POST.get("slot")
        pet_id = request.POST.get("pet")
        pet = get_object_or_404(Pet, pk=pet_id)
        if not pet.owner == request.user:
            return redirect("home")

        Appointment.objects.create(vet_id=owner_id, slot_id=slot_id, pet_id=pet_id)

        return redirect("vets-list")


class UserAppointmentsView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "appointments.view_appointment"
    model = Appointment
    template_name = "accounts/user_appointments.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(vet=self.request.user)
