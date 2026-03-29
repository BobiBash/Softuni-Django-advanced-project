from django.urls import path

from appointments.views import VetScheduleView, UserMakeAppointMentView, UserAppointmentsView

urlpatterns = [
    path('my-appointments', UserAppointmentsView.as_view(), name='appointments'),
    path('<slug:slug>', VetScheduleView.as_view(), name='vet-schedule'),
    path('<slug:slug>/make-appointment', UserMakeAppointMentView.as_view(), name='make-appointment'),
]