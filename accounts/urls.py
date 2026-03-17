from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('register/', views.RegisterOptionsView.as_view(), name='register'),
    path('register-user/', views.RegisterView.as_view(), name='register_user'),
    path('register-vet/', views.RegisterVetView.as_view(), name='register_vet'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('confirm-email/<str:key>/', views.ConfirmEmailView.as_view(), name='confirm-email'),
    path('confirm-vet', TemplateView.as_view(template_name='accounts/confirm_vet.html'), name='confirm-vet'),
    path('email-confirmation',
         TemplateView.as_view(template_name='accounts/email_confirmation.html'),
         name='needed-email-confirmation'),
    path('succesful-confirmation',
         TemplateView.as_view(template_name='accounts/successful_email_confirmation.html'),
         name='successful-email-confirmation')
]