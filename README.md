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

### Development Setup

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

### Production Deployment with Docker

1. Install Docker and Docker Compose on your server

2. Clone the repository:
```bash
git clone https://github.com/ramkumarbalaguruaws/PresalesManagement_Django.git
cd PresalesManagement_Django
```

3. Create .env file with production settings:
```bash
echo "MYSQL_DATABASE=presales
MYSQL_USER=presales
MYSQL_PASSWORD=presales_password
MYSQL_ROOT_PASSWORD=root_password
DJANGO_SECRET_KEY=your-secret-key-here" > .env
```

4. Build and start containers:
```bash
docker-compose up -d --build
```

5. Run initial setup:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py createsuperuser
```

6. The application will be available at http://your-server-ip:8000

### Updating the Application

1. Pull latest changes:
```bash
git pull origin main
```

2. Rebuild and restart containers:
```bash
docker-compose up -d --build
```

3. Run migrations if needed:
```bash
docker-compose exec web python manage.py migrate
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
