# PawMedic - Veterinary Pet Care Platform

A full-featured Django web application for pet owners and veterinarians. PawMedic allows pet owners to manage their pets, book appointments with vets, and participate in a community forum. Veterinarians can manage their profiles, set availability, and interact with the community.

## Features

- **User Authentication** — Registration (pet owner / vet), login, logout, email confirmation, password reset
- **Pet Management** — Full CRUD for pets with photo uploads
- **Vet Profiles** — Detailed vet profiles with specialization, bio, photo, and services offered
- **Appointment System** — Vets manage their schedule; owners book appointments
- **Community Forum** — Create posts, comment, tag posts, edit/delete your content
- **Tag System** — Categorize forum posts with tags for easy filtering
- **Service Management** — Vets can list the services they offer
- **REST API** — Vet search endpoint via Django REST Framework
- **Async Notifications** — Email notifications via Celery + Redis
- **Custom User Model** — Extended with email, phone, role, and custom authentication backend

## Tech Stack

- **Backend:** Django 6.0.3, Django REST Framework 3.17.1
- **Database:** PostgreSQL
- **Async:** Celery + Redis
- **Frontend:** Tailwind CSS, Font Awesome, Flatpickr
- **Styling:** django-tailwind-cli

## Project Structure

```
PawMedic/                 # Main project settings
├── accounts/             # User auth, profiles, groups, permissions
├── appointments/         # Appointment booking and scheduling
├── common/               # Home page and shared utilities
├── forum/                # Community forum (posts, comments, tags)
├── notifications/        # Celery tasks and email notifications
├── pets/                 # Pet management CRUD
├── vets/                 # Vet listing, search, and DRF API
├── templates/            # All HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User-uploaded media files
└── manage.py
```

## Prerequisites

- Python 3.12+
- PostgreSQL
- Redis (for Celery)

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/BobiBash/Softuni-Django-advanced-project.git
cd Softuni-Django-advanced-project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

Create a PostgreSQL database named `pawmedic_db` (or change the name in `.env` and `settings.py`):

```sql
CREATE DATABASE pawmedic_db;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
EMAIL_HOST_USER=your_gmail_address
EMAIL_HOST_PASSWORD=your_gmail_app_password
SECRET_KEY=your_django_secret_key
REDIS_URL=redis://localhost:6379/0
```

> **Note:** For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833). Regular passwords won't work.
>
> **Alternative — MailHog:** For local testing without sending real emails, you can use [MailHog](https://github.com/mailhog/MailHog). Install and run MailHog, then in `settings.py` comment out the Gmail email settings and uncomment the MailHog block (localhost:1025). Emails will be captured in the MailHog web UI at [http://localhost:8025](http://localhost:8025).

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

> Groups ("Vets" and "Pet Owners") with appropriate permissions are created automatically via a `post_migrate` signal.

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### 9. Start Celery (Optional, for async notifications)

In a separate terminal:

```bash
celery -A PawMedic worker --loglevel=info
```

## Optional: Seed the Database

Run the populate script to create sample vet users:

```bash
python populate_db.py
```

## Admin Panel

Access the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) using your superuser credentials.

## User Groups and Permissions

The application defines two user groups with distinct permissions:

| Group | Permissions |
|---|---|
| **Vets** | Manage vet profiles, manage appointment slots, full forum CRUD, manage tags, manage services, view pets |
| **Pet Owners** | Full pet CRUD, full forum CRUD, book and view appointments |

Users are automatically assigned to the correct group based on their role during registration.

## API Endpoints

| Method | URL | Description |
|---|---|---|
| GET | `/vets/api/vets/?search=<query>` | Search published vets (JSON) |

## Database Models

| Model | App | Description |
|---|---|---|
| PawMedicUser | accounts | Custom user model (extends AbstractUser) |
| VetProfile | accounts | Vet profile with services (M2M) |
| Service | accounts | Vet services |
| EmailConfirmation | accounts | Token-based email verification |
| Pet | pets | Pet records with owner FK |
| AppointmentSlot | appointments | Vet availability slots |
| Appointment | appointments | Booked appointments |
| ForumPost | forum | Forum posts with tags (M2M) |
| Tag | forum | Forum post tags |
| Comment | forum | Forum post comments |

### Relationships

- **Many-to-One (FK):** Pet → User, AppointmentSlot → VetProfile, Appointment → Slot/Vet/Pet, ForumPost → User, Comment → Post/User
- **Many-to-Many:** VetProfile ↔ Service, ForumPost ↔ Tag
- **One-to-One:** VetProfile → User, EmailConfirmation → User

## Security

- CSRF protection enabled on all forms
- XSS prevention via Django's auto-escaping
- SQL injection prevention via Django ORM
- Password validation with strength checks
- Email confirmation required for account activation.
- Sensitive credentials stored in environment variables.
- Permission-based access control on all views.

## Deployment

TODO

## Testing

Run the test suite:

```bash
python manage.py test
```

The project includes 28+ tests covering models, forms, and views.

## License

This project was developed as part of the SoftUni Django Advanced course final exam.
