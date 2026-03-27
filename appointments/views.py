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
        print(request.POST )
        date = request.POST.get('date')
        times = request.POST.getlist('time')

        for time in times:
            AppointmentSlot.objects.get_or_create(
                date=date,
                time=time,
                vet_id=request.user.vet_profile
            )
        return redirect('vet-schedule')