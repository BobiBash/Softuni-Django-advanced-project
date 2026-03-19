from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from accounts.validators import validate_password_strength


class PasswordValidationMixin:
    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            if password and check_password(password, self.user.password):
                raise ValidationError('New password cannot be the same as your old password.')
            validate_password_strength(password)
        return self.cleaned_data.get('new_password2')

class AnonymousRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)