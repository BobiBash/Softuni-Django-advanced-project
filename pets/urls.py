from django.urls import path
from django.views.generic import TemplateView, CreateView

from pets.views import AddPet, ListPet, ViewPet, EditPet, DeletePet

urlpatterns = [
    path('', ListPet.as_view(), name='pets'),
    path('add-pet/', AddPet.as_view(), name='add-pet'),
    path('edit-pet/<int:pk>', EditPet.as_view(), name='edit-pet'),
    path('delete-pet/<int:pk>', DeletePet.as_view(), name='delete-pet'),
    path('view-pet/<int:pk>', ViewPet.as_view(), name='view-pet'),
]