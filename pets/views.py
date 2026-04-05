from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from .forms import PetForm
from .models import Pet

# Create your views here.
class ListPet(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'pets.view_pet'
    model = Pet
    template_name = 'pets/pets.html'

    def get_queryset(self):
        return Pet.objects.filter(owner_id=self.request.user.id)

class ViewPet(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = 'pets.view_pet'
    model = Pet
    template_name = 'pets/view-pet.html'

    def get_queryset(self):
        return Pet.objects.filter(owner_id=self.request.user.id)

class AddPet(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'pets.add_pet'
    form_class = PetForm
    template_name = 'pets/add-pet.html'
    success_url = reverse_lazy('pets')

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        print(form)
        return super().form_valid(form)

class EditPet(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'pets.change_pet'
    form_class = PetForm
    template_name = 'pets/edit-pet.html'
    success_url = reverse_lazy('pets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.get_object()
        return context

    def get_queryset(self):
        return Pet.objects.filter(owner_id=self.request.user.id)

class DeletePet(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'pets.delete_pet'
    model = Pet
    template_name = 'pets/delete-pet.html'
    success_url = reverse_lazy('pets')

    def get_queryset(self):
        return Pet.objects.filter(owner_id=self.request.user.id)
