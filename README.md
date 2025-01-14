# Presales Management System

A Django-based web application for managing presales proposals, customers, projects and products.

## Features
- Dashboard with proposal analytics and charts
- CRUD operations for proposals, customers, projects and products
- User authentication and role-based access control
- Export proposals to CSV
- Automated test data generation

## Technology Stack
- Python 3
- Django 4
- SQLite (development)
- Bootstrap 5
- Chart.js

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ramkumarbalaguruaws/PresalesManagement_Django.git
cd PresalesManagement_Django
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Usage

- Access the admin interface at `/admin/`
- Login with your credentials
- Use the dashboard to view proposal analytics
- Manage proposals, customers, projects and products through their respective pages

## Generating Test Data

To generate test proposals:
```bash
python manage.py generate_test_proposals
```

## License
MIT
