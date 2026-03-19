from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView

from .choices import PawMedicUserType
from .forms import RegistrationForm, LoginForm
from .mixins import AnonymousRequiredMixin
from .models import PawMedicUser, EmailConfirmation


# Create your views here.

class RegisterView(CreateView):
    template_name = 'accounts/register_user.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,*args, **kwargs)


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = PawMedicUserType.OWNER
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = PawMedicUserType.OWNER
        user.save()
        token = default_token_generator.make_token(user)
        EmailConfirmation.objects.create(user=user, token=token)
        confirmation_url = self.request.build_absolute_uri(
            reverse('confirm-email', kwargs={'key': token})
        )
        send_mail(
            'Email Confirmation',
            f'Greetings {user.username} you can confirm your email at: %s' % confirmation_url,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect('needed-email-confirmation')



class RegisterVetView(CreateView):
    template_name = 'accounts/register_vet.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


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

class RegisterOptionsView(TemplateView):
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request,*args, **kwargs)

class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    next_page = 'home'



class ConfirmEmailView(View):
    def get(self, request, key):
        confirmation = EmailConfirmation.objects.get(token=key)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return redirect('successful-email-confirmation')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user, user.email, user.role)
        context['profile'] = user
        return context


class VetProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/vet_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user, user.email, user.role)
        context['profile'] = user
        return context

class PawMedicPasswordResetView(AnonymousRequiredMixin, PasswordResetView):
    template_name = 'accounts/password_reset_form.html'




