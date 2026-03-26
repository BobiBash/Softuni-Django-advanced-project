import os
import django
import random
from datetime import date

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PawMedic.settings")
django.setup()

from accounts.models import PawMedicUser, VetProfile
from accounts.choices import PawMedicUserType


def create_vet_users():
    """Create 20 VET users with VetProfile"""

    # List of sample specializations
    specializations = [
        "Small Animal Medicine",
        "Surgery",
        "Dentistry",
        "Dermatology",
        "Cardiology",
        "Oncology",
        "Neurology",
        "Ophthalmology",
        "Emergency & Critical Care",
        "Internal Medicine",
        "Radiology",
        "Anesthesiology",
        "Pathology",
        "Behavioral Medicine",
        "Exotic Animals",
    ]

    # Sample first and last names
    first_names = [
        "James",
        "Mary",
        "John",
        "Patricia",
        "Robert",
        "Jennifer",
        "Michael",
        "Linda",
        "William",
        "Elizabeth",
        "David",
        "Susan",
        "Richard",
        "Jessica",
        "Joseph",
        "Sarah",
        "Thomas",
        "Karen",
        "Charles",
        "Nancy",
        "Christopher",
        "Lisa",
        "Daniel",
        "Margaret",
        "Matthew",
        "Betty",
        "Anthony",
        "Sandra",
        "Donald",
        "Ashley",
    ]

    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
        "Thompson",
        "White",
        "Harris",
        "Sanchez",
        "Clark",
        "Ramirez",
        "Lewis",
        "Robinson",
    ]

    created_users = []

    for i in range(1, 21):
        # Generate unique username and email
        username = f"vet_user_{i}"
        email = f"vet{i}@example.com"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        # Check if user already exists
        if PawMedicUser.objects.filter(username=username).exists():
            print(f"User {username} already exists, skipping...")
            continue

        if PawMedicUser.objects.filter(email=email).exists():
            print(f"Email {email} already exists, skipping...")
            continue

        # Create user
        try:
            user = PawMedicUser.objects.create_user(
                username=username,
                email=email,
                password="vetpassword123",  # Default password
                first_name=first_name,
                last_name=last_name,
                role=PawMedicUserType.VET,
                is_active=True,  # Activate users for testing
            )

            # Create VetProfile
            vet_profile = VetProfile.objects.create(
                user=user,
                specialization=random.choice(specializations),
                years_of_experience=random.randint(1, 30),
                bio=f"Dr. {first_name} {last_name} is a dedicated veterinarian with expertise in their field. They have a passion for animal welfare and providing the best care possible.",
                is_published=True,
            )

            created_users.append((user, vet_profile))
            print(f"Created VET user: {username} ({first_name} {last_name})")
            print(f"  Email: {email}")
            print(f"  Specialization: {vet_profile.specialization}")
            print(f"  Experience: {vet_profile.years_of_experience} years")
            print()

        except Exception as e:
            print(f"Error creating user {username}: {e}")

    return created_users


def print_summary(created_users):
    """Print summary of created users"""
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total VET users created: {len(created_users)}")
    print(f"Total users in database: {PawMedicUser.objects.count()}")
    print(
        f"Total VET users in database: {PawMedicUser.objects.filter(role=PawMedicUserType.VET).count()}"
    )
    print(f"Total VetProfiles: {VetProfile.objects.count()}")

    if created_users:
        print("\nCreated users:")
        for user, profile in created_users:
            print(
                f"  - {user.username}: {user.get_full_name()} ({profile.specialization})"
            )


if __name__ == "__main__":
    print("Starting to populate database with VET users...")
    print("=" * 50)

    created = create_vet_users()
    print_summary(created)

    print("\nDone! All users have password: 'vetpassword123'")
