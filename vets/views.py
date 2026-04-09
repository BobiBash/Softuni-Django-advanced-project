import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.choices import PawMedicUserType
from accounts.models import VetProfile
from appointments.models import AppointmentSlot, Appointment
from pets.models import Pet


# Create your views here.

class VetListView(LoginRequiredMixin, ListView):
    model = VetProfile
    template_name = 'vets/vets-list.html'
    paginate_by = 10

    def get_queryset(self):
        return VetProfile.objects.exclude(is_published=False)

class VetPublishView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'accounts.change_vetprofile'

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != PawMedicUserType.VET:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        vet = request.user.vet_profile
        vet.is_published = not vet.is_published
        vet.save()

        return redirect('vets-list')

class VetDetailView(LoginRequiredMixin, View):
    def get(self, request, slug, pk):
        user = request.user
        vet = get_object_or_404(VetProfile, pk=pk)
        pets = Pet.objects.filter(owner_id=user.id)
        taken_slots = Appointment.objects.values_list('slot_id', flat=True)
        available_slots = (AppointmentSlot.objects.filter(vet_id=pk)
                           .values('id', 'date', 'time')
                           .exclude(id__in=taken_slots))


        context = {
            'user': user,
            'pets': pets,
            'available_slots': available_slots,
            'available_slots_json': json.dumps(list(available_slots), default=str),
            "vet": vet,
        }

        return render(request, 'vets/vets-detail.html', context)

class VetSearchView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('search', '')
        print(query)
        vets_found = (VetProfile
                      .objects
                      .filter
                      (Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
                      .exclude(is_published=False))

        paginator = Paginator(vets_found, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'query': query,
            'vets': vets_found,
            'page_obj': page_obj,
        }

        return render(request, 'vets/vet-search.html', context)




