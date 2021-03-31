import codecs
import csv

from django.core.management.base import BaseCommand

import requests

from drnalpha.sic_codes.models import Code

SRC = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/527619/SIC07_CH_condensed_list_en.csv"  # noqa


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Perform a dry run without saving any data.",
        )
        parser.add_argument(
            "-c",
            "--clear",
            action="store_true",
            help="Clear existing data.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        clear = options["clear"]

        self.stdout.write("Importing SIC codes...")

        if clear:
            deleted_count, _ = Code.objects.all().delete()
            self.stdout.write(self.style.WARNING("Deleted: {:d}".format(deleted_count)))

        response = requests.get(SRC, stream=True)
        response.raise_for_status()

        reader = csv.reader(
            codecs.iterdecode(response.iter_lines(), "utf-8"), delimiter=","
        )
        count = 0

        for row in reader:
            if count > 0:
                code = int(row[0])
                title = row[1].strip().capitalize()

                if dry_run:
                    self.style.SUCCESS("Found: {:d} {}".format(code, title))

                else:
                    obj, created = Code.objects.update_or_create(code=code, title=title)

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                "Created: {:d} {}".format(obj.code, obj.title)
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.NOTICE(
                                "Updated: {:d} {}".format(obj.code, obj.title)
                            )
                        )

            count += 1

        if not dry_run:
            self.stdout.write(self.style.SUCCESS("Imported: {:d}".format(count)))
