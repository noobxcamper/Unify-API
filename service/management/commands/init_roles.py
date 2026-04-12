from django.core.management.base import BaseCommand
from core.models import Roles

class Command(BaseCommand):
    help = "Seed default roles into the database"

    def handle(self, *args, **kwargs):
        roles = [
            "User",
            "Admin",
            "IT",
            "HR",
            "Automation Administrator",
        ]

        for role in roles:
            obj, created = Roles.objects.get_or_create(name=role)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role}"))
            else:
                self.stdout.write(f"Role already exists: {role}")

        self.stdout.write(self.style.SUCCESS("Init complete."))
