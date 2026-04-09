from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views
from .forms import (
    PawMedicPasswordResetForm,
    PawMedicPasswordChangeForm,
    PawMedicUserPasswordReset,
)
from .views import PawMedicPasswordResetView

urlpatterns = [
    path('register/', views.RegisterOptionsView.as_view(), name='register'),
    path('register-user/', views.RegisterView.as_view(), name='register_user'),
    path('register-vet/', views.RegisterVetView.as_view(), name='register_vet'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            form_class=PawMedicPasswordChangeForm,
            success_url=reverse_lazy('password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password-change-complete/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_complete.html'
        ),
        name='password_change_done',
    ),
    path(
        'password-reset/',
        PawMedicPasswordResetView.as_view(
            form_class=PawMedicUserPasswordReset,
        ),
        name='password-reset',
    ),
    path(
        'password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            form_class=PawMedicPasswordResetForm,
            template_name='accounts/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('vet-profile/', views.VetProfileView.as_view(), name='vet-profile'),
    path(
        'confirm-email/<str:key>/',
        views.ConfirmEmailView.as_view(),
        name='confirm-email',
    ),
    path(
        'confirm-vet',
        TemplateView.as_view(template_name='accounts/confirm_vet.html'),
        name='confirm-vet',
    ),
    path(
        'email-confirmation',
        TemplateView.as_view(template_name='accounts/email_confirmation.html'),
        name='needed-email-confirmation',
    ),
    path(
        'succesful-confirmation',
        TemplateView.as_view(
            template_name='accounts/successful_email_confirmation.html'
        ),
        name='successful-email-confirmation',
    ),
    path(
        'vet/update-photo/',
        views.UpdateProfilePhotoView.as_view(),
        name='update-vet-photo',
    ),
    path(
        'vet/update-bio/', views.UpdateProfileBioView.as_view(), name='update-vet-bio'
    ),
    path('vet/<int:pk>/favorite', views.AddFavoriteVet.as_view(), name='add-favoriteVet'),
    path('favorites-list', views.UserFavorites.as_view(), name='user-favorites'),
path('favorited_by-list', views.VetFavoritedBy.as_view(), name='vet-favorited_by')
]