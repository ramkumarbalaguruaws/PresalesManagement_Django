from django.core.management.base import BaseCommand
from users.models import User, Proposal, Project, Customer
from datetime import datetime, timedelta
import random
from faker import Faker


class Command(BaseCommand):
    help = (
        "Generates comprehensive test data including customers, projects and proposals"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of proposals to generate (default: 10)",
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]

        # Create admin user if not exists
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "password": "admin",
                "role": "ADMIN",
            },
        )

        # Create list of sales directors
        sales_directors = [
            "John Smith",
            "Emily Johnson",
            "Michael Brown",
            "Sarah Davis",
            "David Wilson",
            "Jessica Martinez",
            "Daniel Anderson",
            "Laura Taylor",
            "James Thomas",
            "Karen Garcia",
        ]

        # Create test presales user
        presales_user, _ = User.objects.get_or_create(
            username="presales",
            defaults={
                "email": "presales@example.com",
                "password": "presales123",
                "role": "PRESALES",
            },
        )

        # Create test viewer user
        viewer_user, _ = User.objects.get_or_create(
            username="viewer",
            defaults={
                "email": "viewer@example.com",
                "password": "viewer123",
                "role": "VIEWER",
            },
        )

        # Create 3 main customers
        customers = []
        for i in range(3):
            customer = Customer.objects.create(
                name=fake.company(),
                contact_details=fake.paragraph(),
                remarks=fake.sentence(),
            )
            customers.append(customer)
            self.stdout.write(f"Created customer: {customer.name}")

            # Create 2-4 projects per customer
            for j in range(random.randint(2, 4)):
                project = Project.objects.create(
                    project_name=f"{customer.name} Project {j+1}",
                    customer=customer,
                    country=fake.country(),
                    link=fake.url(),
                )
                self.stdout.write(f"  Created project: {project.project_name}")

                # Create 2-3 proposals per project
                for k in range(random.randint(2, 3)):
                    proposal = Proposal.objects.create(
                        project=project,
                        priority=random.choice(["P1", "P2", "P3"]),
                        bandwidth=f"{random.choice([100, 200, 500])}Mbps",
                        gateway=random.choice(["JAV", "SUB", "BHI", "PAK"]),
                        terminal_count=random.randint(1, 20),
                        terminal_type=random.choice(
                            ["1m2_3W_MDM2510", "1m8_5W_MDM2510", "2m4_8W_MDM2510"]
                        ),
                        customer=customer.name,
                        sales_director=random.choice(sales_directors),
                        presales_owner=presales_user.email,
                        submission_date=datetime.now()
                        + timedelta(days=random.randint(1, 90)),
                        proposal_link=fake.url(),
                        commercial_value=random.uniform(10000, 500000),
                        status=random.choice(["ONGOING", "BLOCKED", "CLOSED"]),
                        remarks=fake.paragraph(),
                        created_by=random.choice(
                            [admin_user, presales_user, viewer_user]
                        ),
                    )
                    self.stdout.write(
                        f"    Created proposal: {proposal.project.project_name} - {proposal.get_status_display()}"
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created test data with {count} proposals")
        )
