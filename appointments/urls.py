from django.urls import path

from appointments.views import VetScheduleView, UserAppointMentView

urlpatterns = [
    path('<slug:slug>', VetScheduleView.as_view(), name='vet-schedule'),
    path('<slug:slug>/make-appointment', UserAppointMentView.as_view(), name='make-appointment')
]