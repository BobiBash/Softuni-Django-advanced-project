from django.urls import path

from appointments.views import VetScheduleView

urlpatterns = [
    path('', VetScheduleView.as_view(), name='vet-schedule'),
]