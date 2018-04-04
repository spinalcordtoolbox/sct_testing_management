from django.core.management.base import BaseCommand

from sct_annotation.annotations.models import Image, LabeledImage


class Command(BaseCommand):
    """Update the filestate field in the Image and LabeledImage tables"""

    def _check_images(self, rows):
        for row in rows:
            row.save()
            if hasattr(row, 'error_msg'):
                self.stderr.write(row.error_msg)

    def handle(self, *args, **kwargs):
        rows = Image.objects.all()
        self._check_images(rows)

        rows = LabeledImage.objects.all()
        self._check_images(rows)
