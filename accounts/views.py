from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView, ListView,
)

from .choices import PawMedicUserType
from .forms import RegistrationForm, LoginForm, VetProfileForm
from .mixins import AnonymousRequiredMixin
from .models import EmailConfirmation, VetProfile, FavoriteVet


# Create your views here.


class RegisterView(CreateView):
    template_name = "accounts/register_user.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    # check if user is authenticated
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["role"] = PawMedicUserType.OWNER
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = PawMedicUserType.OWNER
        user.save()
        token = default_token_generator.make_token(user)
        EmailConfirmation.objects.create(user=user, token=token)
        confirmation_url = self.request.build_absolute_uri(
            reverse("confirm-email", kwargs={"key": token})
        )
        send_mail(
            "Email Confirmation",
            f"Greetings {user.username} you can confirm your email at: %s"
            % confirmation_url,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        return redirect("needed-email-confirmation")


class RegisterVetView(View):
    template_name = "accounts/register_vet.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user_form = RegistrationForm(role=PawMedicUserType.VET)
        vet_form = VetProfileForm()
        context = {"form": user_form, "vet_form": vet_form}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = RegistrationForm(
            request.POST, request.FILES, role=PawMedicUserType.VET
        )
        vet_form = VetProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and vet_form.is_valid():
            user = user_form.save(commit=False)
            user.role = PawMedicUserType.VET
            user.is_active = True
            user.save()

            vet_profile = vet_form.save(commit=False)
            vet_profile.user = user
            vet_profile.save()

            return redirect("confirm-vet")

        context = {"form": user_form, "vet_form": vet_form}

        return render(request, self.template_name, context)

class RegisterOptionsView(TemplateView):
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    next_page = 'home'


class ConfirmEmailView(View):
    def get(self, request, key):
        confirmation = get_object_or_404(EmailConfirmation, token=key)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return redirect('successful-email-confirmation')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user, user.email, user.role)
        context["profile"] = user
        return context


class VetProfileView(LoginRequiredMixin, TemplateView):
    model = VetProfile
    template_name = "accounts/vet_profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != PawMedicUserType.VET:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vet = user.vet_profile
        context['profile'] = user
        context['vet'] = vet
        return context

class PawMedicPasswordResetView(AnonymousRequiredMixin, PasswordResetView):
    template_name = 'accounts/password_reset_form.html'


class UpdateProfilePhotoView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != PawMedicUserType.VET:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        vet = request.user.vet_profile
        vet.photo = request.FILES.get('photo')
        vet.save()
        return redirect('vet-profile')

class UpdateProfileBioView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != PawMedicUserType.VET:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        vet = request.user.vet_profile
        vet.bio = request.POST.get('bio')
        vet.save()
        return redirect('vet-profile')

class AddFavoriteVet(LoginRequiredMixin, View):

    def post(self, request, pk):
        owner_id = request.user.id
        print(pk)
        vet = get_object_or_404(VetProfile, pk=pk)
        favorite = FavoriteVet.objects.filter(owner_id=owner_id, vet=vet).first()

        if favorite:
            favorite.delete()
        else:
            FavoriteVet.objects.create(
                owner_id=owner_id,
                vet_id=vet.pk
            )

        return redirect('vets-detail', slug=vet.slug, pk=vet.pk)


class UserFavorites(LoginRequiredMixin, ListView):
    model = FavoriteVet
    template_name = 'accounts/favorite_vets.html'
    paginate_by = 10


class VetFavoritedBy(LoginRequiredMixin, ListView):
    model = FavoriteVet
    template_name = 'accounts/favorited_by.html'
    paginate_by = 10