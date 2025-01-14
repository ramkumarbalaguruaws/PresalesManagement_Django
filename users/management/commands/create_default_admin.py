from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates the default admin user'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                first_name='Admin',
                last_name='User',
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created default admin user'))
        else:
            self.stdout.write('Default admin user already exists')
