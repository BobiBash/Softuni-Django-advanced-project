from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from accounts.models import PawMedicUser
from pets.models import Pet
from pets.forms import PetForm


class PetModelTest(TestCase):
    def setUp(self):
        self.user = PawMedicUser.objects.create_user(
            username="petowner",
            email="owner@example.com",
            password="TestPass123",
            first_name="Owner",
            last_name="User",
            is_active=True,
        )

    def test_create_pet(self):
        pet = Pet.objects.create(
            owner=self.user,
            name="Buddy",
            species="Dog",
            breed="Golden Retriever",
            date_of_birth=date(2020, 1, 1),
        )
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner, self.user)

    def test_pet_date_of_birth_validation(self):
        future_date = date.today() + timedelta(days=30)
        form_data = {
            "name": "FuturePet",
            "species": "Cat",
            "breed": "Persian",
            "date_of_birth": future_date,
        }
        form = PetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("date_of_birth", form.errors)


class PetFormTest(TestCase):
    def setUp(self):
        self.user = PawMedicUser.objects.create_user(
            username="petowner",
            email="owner@example.com",
            password="TestPass123",
            is_active=True,
        )

    def test_valid_pet_form(self):
        form_data = {
            "name": "Max",
            "species": "Dog",
            "breed": "Labrador",
            "date_of_birth": "2020-05-15",
        }
        form = PetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pet_form_missing_name(self):
        form_data = {
            "name": "",
            "species": "Dog",
            "breed": "Labrador",
            "date_of_birth": "2020-05-15",
        }
        form = PetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_pet_form_future_date(self):
        future_date = date.today() + timedelta(days=30)
        form_data = {
            "name": "Max",
            "species": "Dog",
            "breed": "Labrador",
            "date_of_birth": future_date,
        }
        form = PetForm(data=form_data)
        self.assertFalse(form.is_valid())
