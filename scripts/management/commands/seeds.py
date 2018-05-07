from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.job.models import Job
from apps.organization.models import Organization
from code_sample import settings
from libs.utils import get_random_int, get_random_between_given

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

        organizations = []
        organizations.append(Organization.objects.create(name='Organization A', description='Lorem Ipsum'))
        organizations.append(Organization.objects.create(name='Organization B', description='Lorem Ipsum'))

        for i in range(1000):
            Job.objects.create(
                title='Job ' + str(get_random_int()),
                description='lorem Ipsum',
                organization=organizations[get_random_between_given(0, 1)]
            )

        self.stdout.write("Organizations & Jobs added successfully...")

        self.stdout.write("Task Successful")
