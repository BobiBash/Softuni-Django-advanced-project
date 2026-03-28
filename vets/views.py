from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.choices import PawMedicUserType
from accounts.models import VetProfile
from appointments.models import AppointmentSlot
from pets.models import Pet


# Create your views here.

class VetListView(LoginRequiredMixin, ListView):
    model = VetProfile
    template_name = 'vets/vets-list.html'
    paginate_by = 10

    def get_queryset(self):
        return VetProfile.objects.exclude(photo__isnull=True).exclude(photo__exact='').exclude(is_published=False)

class VetPublishView(LoginRequiredMixin, View):
    def post(self, request):
        vet = request.user.vet_profile
        vet.is_published = not vet.is_published
        vet.save()

        return redirect('vets-list')

class VetDetailView(LoginRequiredMixin, View):
    def get(self, request, slug, pk):
        user = request.user
        print(user)
        pets = Pet.objects.filter(owner_id=user.id)
        print(user.id)
        print(pets)
        available_slots = AppointmentSlot.objects.filter(vet_id=pk)
        print(pk)
        print(available_slots)

        context = {
            'user': user,
            'pets': pets,
            'slots': available_slots,
        }

        return render(request, 'vets/vets-detail.html', context)



