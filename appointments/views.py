from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
import json
from appointments.models import AppointmentSlot


# Create your views here.
class VetScheduleView(LoginRequiredMixin, View):
    def get(self, request):
        slots = AppointmentSlot.objects.filter(
            vet_id=request.user.vet_profile
        ).values('date', 'time')

        return render(request, 'appointments/manage_schedule.html', {
        'slots': json.dumps(list(slots), default=str)
    })

    def post(self, request):
        vet_id = request.user.vet_profile.id
        print(vet_id)
        date = request.POST.get('date')
        times = request.POST.getlist('time')
        AppointmentSlot.objects.filter(vet_id=vet_id).delete()

        for time in times:
            AppointmentSlot.objects.get_or_create(
                date=date,
                time=time,
                vet_id=vet_id
            )
        return redirect('vet-schedule')