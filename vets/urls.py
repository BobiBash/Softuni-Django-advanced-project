from django.urls import path

from vets.views import VetListView, VetPublishView, VetDetailView

urlpatterns = [
    path('', VetListView.as_view(), name='vets-list'),
    path('<slug:slug>/<int:pk>', VetDetailView.as_view(), name='vets-detail'),
    path('publish-vet', VetPublishView.as_view(), name='publish-vet'),
]