from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordResetForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError
from django import forms
from .mixins import PasswordValidationMixin, AnonymousRequiredMixin
from .models import PawMedicUser, VetProfile
from .validators import validate_password_strength, validate_username_taken


class RegistrationForm(UserCreationForm):
    class Meta:
        model = PawMedicUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "phone",
        )

    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "outline-none w-60"
            self.fields[field].help_text = None
            self.fields[field].error_messages = {
                "required": f"This field is required.",
            }

        self.fields["phone"].required = False

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validate_username_taken(username)
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        validate_password_strength(password1)
        return password1


class VetProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "outline-none w-60"
            self.fields[field].help_text = None
            self.fields[field].error_messages = {
                "required": f"This field is required.",
            }

    class Meta:
        model = VetProfile
        fields = ("specialization", "years_of_experience", "bio", "photo")

        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 6,
                    "cols": 25,
                    "style": "resize:none",
                    "class": "focus:outline-none",
                }
            ),
            "years_of_experience": forms.NumberInput(attrs={}),
        }


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Invalid username/email or password.",
        "inactive": "Please confirm your email.",
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "outline-none"

        self.fields["username"].error_messages = {
            "required": "Please enter your username or email.",
        }
        self.fields["password"].error_messages = {
            "required": "Please enter your password.",
        }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )


class PawMedicUserPasswordReset(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].error_messages = {
            "required": "Please enter your email address to reset your password.",
            "invalid": "Please enter a valid email address.",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not PawMedicUser.objects.filter(email=email).exists():
            raise ValidationError("No account with this email exists")

        return email


class PawMedicPasswordResetForm(AnonymousRequiredMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].validators = []

        self.fields["new_password1"].error_messages = {
            "required": "This field is required.",
            "invalid": "Please enter a valid password.",
        }

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")
        if password:
            validate_password_strength(password)
        return password

    def clean(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")

        return self.cleaned_data

    def _post_clean(self):
        pass


class PawMedicPasswordChangeForm(PasswordValidationMixin, PasswordChangeForm):
    pass
