from django.urls import path

from vets.views import VetListView

urlpatterns = [
    path('', VetListView.as_view(), name='vet-list'),
]