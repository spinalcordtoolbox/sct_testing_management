from pathlib import Path
import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from annotations.models import (History, Dataset)


class Command(BaseCommand):
    help = 'Import all the json files into a database'

    def handle(self, *args, **kwargs):
        root = Path('/Volumes/sct_testing/large')
        datasets = (x for x in root.glob('*/dataset_description.json'))
        for dataset in datasets:
            self.stdout.write('Reading record %s' % str(dataset))
            data = json.load(open(dataset))
            subject = Dataset.objects.get(path=str(dataset.parent))
            try:
                mod_date = timezone.localtime(
                    datetime.fromtimestamp(
                        os.path.getmtime(str(dataset))))
                obj, created = History.objects.get_or_create(
                    dataset=subject,
                    modified_date=mod_date,
                    center=data['Center'],
                    subject=data['Subject'],
                    study=data['Study'],
                    pathology=data['Pathology'],
                    pam50=data.get('PAM50', 'NA'),
                    gm_model=data.get('gm_model', 'NA'))
            except KeyError:
                raise CommandError('Error in the json file %s' % str(dataset))

            if created:
                self.stdout.write('Created %s' % dataset)
            else:
                self.stdout.write('Skipping %s' % dataset)
