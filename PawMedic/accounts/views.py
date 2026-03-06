from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView
from simple_email_confirmation.models import EmailAddress

from .choices import PawMedicUserType
from .forms import RegistrationForm, LoginForm
from .models import PawMedicUser


# Create your views here.

class RegisterView(CreateView):
    template_name = 'accounts/register_user.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = PawMedicUserType.OWNER
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = PawMedicUserType.OWNER
        user.save()

        confirmation_key = user.add_email_if_not_exists(user.email)
        confirmation_url = self.request.build_absolute_uri(
            reverse('confirm-email', kwargs={'key': confirmation_key})
        )
        send_mail(
            'Confirm your Email',
            'Click this link to confirm your email: %s' % confirmation_url,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect('home')



class RegisterVetView(CreateView):
    template_name = 'accounts/register_vet.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = PawMedicUserType.VET
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = PawMedicUserType.VET
        """
        Set user.is_active to True for testing permissions etc. but the idea is that
        the legitimacy of registered Veterinarians gets confirmed via a call by staff members
        to ask additional information.
        """
        user.is_active = True
        user.save()
        return redirect('confirm-vet')

class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm



class ConfirmEmailView(View):
    def get(self, request, key):
        email = EmailAddress.objects.get(key=key)
        user = email.user
        user.confirm_email(key)
        user.is_active = True
        user.save()
        return redirect('login')






