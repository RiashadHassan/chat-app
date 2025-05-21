from tqdm import tqdm

from django.db import transaction
from django.core.management import BaseCommand

from ...models import Permission
from ...constants import PERMISSIONS


class Command(BaseCommand):
    help = "Create Permissions from permissions/constants.py module"

    def handle(self, *args, **options):
        existing_permissions = set(Permission.objects.values_list("name", flat=True))
        new_permissions = set(PERMISSIONS) - existing_permissions

        if not new_permissions:
            self.stdout.write(self.style.SUCCESS("All permissions already exist."))
            return

        with transaction.atomic():
            permissions_to_create = [
                Permission(name=permission)
                for permission in tqdm(new_permissions, desc="Creating Permissions...")
            ]

            Permission.objects.bulk_create(permissions_to_create, ignore_conflicts=True)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(new_permissions)} permissions."
            )
        )
