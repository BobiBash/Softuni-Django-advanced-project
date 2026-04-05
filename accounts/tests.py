from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import PawMedicUser, VetProfile, EmailConfirmation
from accounts.choices import PawMedicUserType
from accounts.forms import RegistrationForm, VetProfileForm, LoginForm


class PawMedicUserModelTest(TestCase):
    def test_create_user(self):
        user = PawMedicUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_active)

    def test_get_fullname(self):
        user = PawMedicUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.get_fullname(), "John Doe")

    def test_default_role_is_owner(self):
        user = PawMedicUser.objects.create_user(
            username="testuser", email="test@example.com", password="TestPass123"
        )
        self.assertEqual(user.role, PawMedicUserType.OWNER)


class VetProfileModelTest(TestCase):
    def setUp(self):
        self.user = PawMedicUser.objects.create_user(
            username="vetuser",
            email="vet@example.com",
            password="TestPass123",
            first_name="Dr",
            last_name="Smith",
            role=PawMedicUserType.VET,
            is_active=True,
        )
        self.vet_profile = VetProfile.objects.create(
            user=self.user,
            specialization="Surgery",
            years_of_experience=10,
            bio="Experienced vet surgeon",
        )

    def test_vet_profile_creation(self):
        self.assertEqual(self.vet_profile.specialization, "Surgery")
        self.assertEqual(self.vet_profile.years_of_experience, 10)
        self.assertFalse(self.vet_profile.is_published)

    def test_vet_profile_get_fullname(self):
        self.assertEqual(self.vet_profile.get_fullname(), "Dr Smith")


class RegistrationFormTest(TestCase):
    def test_valid_registration(self):
        form_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "first_name": "New",
            "last_name": "User",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_password_mismatch(self):
        form_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123",
            "password2": "DifferentPass456",
            "first_name": "New",
            "last_name": "User",
            "phone": "",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_weak_password(self):
        form_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "weak",
            "password2": "weak",
            "first_name": "New",
            "last_name": "User",
            "phone": "",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class VetProfileFormTest(TestCase):
    def test_valid_vet_profile_form(self):
        form_data = {
            "specialization": "Dermatology",
            "years_of_experience": 5,
            "bio": "Specialist in animal skin conditions",
        }
        form = VetProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vet_profile_form_missing_fields(self):
        form_data = {
            "specialization": "",
            "years_of_experience": "",
            "bio": "",
        }
        form = VetProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):
    def test_login_form_invalid_credentials(self):
        form = LoginForm(data={"username": "testuser", "password": "testpass"})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
