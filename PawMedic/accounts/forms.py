from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import PawMedicUser
from .validators import validate_password_strength, validate_username_taken
from .choices import PawMedicUserType


class RegistrationForm(UserCreationForm):
    class Meta:
        model = PawMedicUser
        fields = ('username', 'email', 'password1', 'password2', 'phone')


    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)

        if role != PawMedicUserType.VET:
            self.fields.pop('phone')

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'outline-none w-100%'
            self.fields[field].help_text = None
            self.fields[field].error_messages = {
                 'required': f'This field is required.',
            }


    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username_taken(username)
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password_strength(password1)
        return password1


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Invalid username/email or password.",
        'inactive': "Please confirm your email.",
    }
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'outline-none'

        self.fields['username'].error_messages = {
            'required': 'Please enter your username or email.',
        }
        self.fields['password'].error_messages = {
            'required': 'Please enter your password.',
        }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(self.error_messages['inactive'],
                                  code='inactive',)




