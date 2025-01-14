from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Creates a test Presales user'

    def handle(self, *args, **options):
        # Create test Presales user
        user, created = User.objects.get_or_create(
            username='test',
            defaults={
                'email': 'test@example.com',
                'role': 'PRESALES',
                'is_staff': True,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('test123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Successfully created test Presales user'))
        else:
            self.stdout.write(self.style.WARNING('Test user already exists'))
