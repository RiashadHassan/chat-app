from tqdm import tqdm

from django.db import transaction
from django.core.management import BaseCommand

from ...models import Spectrum
from ...constants import STATIC_SPECTRUM_LIST


class Command(BaseCommand):
    help = "Create Spectra from core/constants.py module"

    def handle(self, *args, **options):
        existing_names = set(Spectrum.objects.values_list("name", flat=True))
        new_spectra = [
            (name, desc)
            for name, desc in STATIC_SPECTRUM_LIST
            if name not in existing_names
        ]

        if not new_spectra:
            self.stdout.write(self.style.SUCCESS("All spectra already exist."))
            return

        with transaction.atomic():
            spectra_to_create = [
                Spectrum(name=name, description=desc)
                for name, desc in tqdm(new_spectra, desc="Creating Spectra...")
            ]
            Spectrum.objects.bulk_create(spectra_to_create, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(spectra_to_create)} spectra."
            )
        )
