from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('register/', TemplateView.as_view(template_name='accounts/register.html'), name='register'),
    path('register-user/', views.RegisterView.as_view(), name='register_user'),
    path('register-vet/', views.RegisterVetView.as_view(), name='register_vet'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='confirm-email'),
    path('confirm-vet', TemplateView.as_view(template_name='accounts/confirm_vet.html'), name='confirm-vet')
]