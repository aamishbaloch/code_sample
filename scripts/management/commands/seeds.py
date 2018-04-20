from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from code_sample import settings

User = get_user_model()


class SeedsConstants:
    pass


class Command(BaseCommand):
    help = "Add mandatory data."

    def handle(self, *args, **options):
        User.objects.create_superuser(
            password=settings.SUPERUSER_PASSWORD,
            email=settings.SUPERUSER_EMAIL
        )
        self.stdout.write("Super User created successfully...")

        self.stdout.write("Task Successful")
