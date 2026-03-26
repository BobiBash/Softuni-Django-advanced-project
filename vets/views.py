from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from accounts.choices import PawMedicUserType
from accounts.models import VetProfile
from pets.models import Pet


# Create your views here.

class VetListView(LoginRequiredMixin, ListView):
    model = VetProfile
    template_name = 'vets/vets-list.html'
    paginate_by = 10

    def get_queryset(self):
        return VetProfile.objects.exclude(photo__isnull=True).exclude(photo__exact='')