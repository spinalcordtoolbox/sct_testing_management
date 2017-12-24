import os
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from annotations.models import Dataset, Contrast


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        root = Path('/Volumes/sct_testing/large')
        contrasts = (x for x in root.glob('*/*/segmentation_description.json'))

        for contrast in contrasts:
            self.stdout.write('Reading segmentation description %s' % str(contrast))
            parent = contrast.parent
            dataset = Dataset.objects.get(path=str(parent.parent))
            name = parent.parts[-1]
            create_date = timezone.localtime(
                datetime.fromtimestamp(
                    os.path.getmtime(str(parent))))

            model = Contrast(dataset=dataset,
                             contrast=name,
                             create_date=create_date)
            model.save()
