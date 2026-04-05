from django.test import TestCase
from datetime import date, time
from accounts.models import PawMedicUser, VetProfile
from pets.models import Pet
from appointments.models import AppointmentSlot, Appointment


class AppointmentSlotModelTest(TestCase):
    def setUp(self):
        self.vet_user = PawMedicUser.objects.create_user(
            username="vetuser",
            email="vet@example.com",
            password="TestPass123",
            first_name="Dr",
            last_name="Vet",
            role="VET",
            is_active=True,
        )
        self.vet_profile = VetProfile.objects.create(
            user=self.vet_user,
            specialization="General",
            years_of_experience=5,
            bio="Test vet bio",
        )

    def test_create_appointment_slot(self):
        slot = AppointmentSlot.objects.create(
            vet=self.vet_profile, date=date(2026, 5, 1), time=time(10, 0)
        )
        self.assertEqual(slot.date, date(2026, 5, 1))
        self.assertEqual(slot.time, time(10, 0))
        self.assertFalse(slot.is_booked)

    def test_slot_default_not_booked(self):
        slot = AppointmentSlot.objects.create(
            vet=self.vet_profile, date=date(2026, 5, 1), time=time(14, 30)
        )
        self.assertFalse(slot.is_booked)


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.owner = PawMedicUser.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="TestPass123",
            is_active=True,
        )
        self.vet_user = PawMedicUser.objects.create_user(
            username="vet",
            email="vet@example.com",
            password="TestPass123",
            first_name="Dr",
            last_name="Vet",
            role="VET",
            is_active=True,
        )
        self.vet_profile = VetProfile.objects.create(
            user=self.vet_user,
            specialization="Surgery",
            years_of_experience=10,
            bio="Experienced vet",
        )
        self.pet = Pet.objects.create(
            owner=self.owner,
            name="Buddy",
            species="Dog",
            breed="Labrador",
            date_of_birth=date(2020, 1, 1),
        )
        self.slot = AppointmentSlot.objects.create(
            vet=self.vet_profile, date=date(2026, 5, 1), time=time(10, 0)
        )

    def test_create_appointment(self):
        appointment = Appointment.objects.create(
            slot=self.slot, vet=self.owner, pet=self.pet
        )
        self.assertEqual(appointment.pet, self.pet)
        self.assertEqual(appointment.slot, self.slot)

    def test_appointment_relationships(self):
        appointment = Appointment.objects.create(
            slot=self.slot, vet=self.owner, pet=self.pet
        )
        self.assertEqual(appointment.vet, self.owner)
        self.assertEqual(appointment.pet.name, "Buddy")
