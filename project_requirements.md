# Django Advanced Regular Exam — Individual Project

> Build a functional, visually appealing, and production-ready web application demonstrating advanced Django concepts and RESTful API development.

---

## Core Functional Requirements

- Public section (anonymous users) and private section (authenticated users only)
- User registration, login, and logout
- At least **two user groups** defined in admin with distinct permissions
- Built-in Django User model must be **extended**

---

## Technical Stack

- Django and/or Django REST Framework (latest stable versions)
- At least **5 Django apps** with clearly defined responsibilities
- At least **5 database models**
  - Models via inheritance or one-to-one relationships count as one model
  - At least **2 many-to-one** and **2 many-to-many** relationships

---

## Forms and Validations

- At least **7 forms** with proper data validations
- Display user-friendly error messages for invalid input
- Validations in both models and forms where appropriate
- Customize error messages, help texts, labels, and placeholders
- At least **2 forms** must include read-only or disabled fields
- Exclude unnecessary fields when rendering forms
- Confirmation step before deleting any object

---

## Views and APIs

- Use **Class-Based Views (CBVs)** as the main approach (~90% CBVs)
- Handle forms correctly (GET and POST, validation, saving)
- Use redirects after successful create/update actions
- At least **one RESTful API endpoint** using Django REST Framework
  - Use serializers, API views, and permissions appropriately

---

## Templates and Frontend

- At least **15 web pages/templates** using Django Template Engine or a frontend framework
  - At least **10** must display dynamic data from the database
- Full **CRUD functionality** for at least **3 models** (manageable by owners)
- Include pages for: all objects, filtered/sorted objects, single-object details, user profiles
- Built-in and **custom template filters/tags**
- Custom error pages (404, 500, etc.)
- Base template (not counted in the 15)
- Template inheritance and reusable partial templates
- Navigation links connecting all pages — no orphan pages
- Show/hide links for anonymous vs authenticated users
- Responsive design using Bootstrap, AI-generated layout, or custom design
- Consistent navigation menus and footers across all pages

---

## Additional Technical Requirements

- **Asynchronous task processing** (Celery, RQ, or asyncio-based)
- Security and data protection:
  - Prevent SQL injection, XSS, CSRF, and parameter tampering
  - Use environment variables for sensitive data (no hardcoded secrets)
- Use **PostgreSQL** or another relational database
- Store and serve media and static files properly
- At least **15 tests** covering custom logic, views, and user-related functionality
- **Deploy** on a cloud-based platform (project evaluated on deployed version)
- Use **GitHub** for version control
  - Public repository
  - Minimum **7 commits on 7 separate days**

---

## Documentation and Code Quality

- Comprehensive GitHub README with setup, dependencies, and deployment info
- Environment setup instructions and sample `.env` configuration
- Follow OOP and clean code principles:
  - Data encapsulation and proper exception handling
  - Inheritance, abstraction, and polymorphism where relevant
  - Strong cohesion and loose coupling
  - Readable, well-formatted code with clear naming conventions

---

## Disclaimer

- **NOT allowed:**
  - Ideas, models, HTML, CSS, or entire apps from SoftUni workshops/lectures
  - HTML/CSS/JS from JS modules or other SoftUni courses
  - AI-generated code (except HTML/CSS layouts or documentation)
- Projects over **60% AI-generated** will be disqualified (0 points)

---

## Submission Deadline

- Submit GitHub repository link before **15:59 on 07 April 2026**
- Submission button available from **31 March 2026**
- Do not push new commits after submission until evaluation is complete
- Assessment takes up to **10 days** (results around 16 April 2026)

---

## Assessment Criteria

| Category | Points |
|----------|--------|
| Originality and Concept | 10 |
| Database Design and Relationships | 5 |
| User Model, Groups/Permissions, Authentication | 5 |
| Forms, Validation, Media Files | 5 |
| Views Implementation (CBVs, mixins, advanced) | 10 |
| Pages (design, navigation, dynamic data) | 10 |
| Asynchronous Processing | 10 |
| RESTful APIs (serializers, permissions, integration) | 10 |
| Deployment and Environment Configuration | 10 |
| Tests (minimum 15, coverage and correctness) | 5 |
| Security, Data Protection, Advanced Features | 10 |
| Project Documentation | 4 |
| Version Control (Git discipline) | 3 |
| Code Quality and Architecture | 3 |
| **Total** | **100** |
