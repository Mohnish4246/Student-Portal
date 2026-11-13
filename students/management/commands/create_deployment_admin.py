
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a deployment administrator account."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            raise CommandError(
                "DJANGO_SUPERUSER_USERNAME and "
                "DJANGO_SUPERUSER_PASSWORD are required."
            )

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User '{username}' already exists. No changes made."
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{user.username}' created successfully."
            )
        )
