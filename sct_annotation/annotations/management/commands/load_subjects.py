"""Scrape the root sct_testing folder and populate the DB.

Using the folder structure as the single source of true, I populate

From what deduce is the dataset = [center]_[study]_[subject]/[contrast]

"""

import json
import logging
import pandas as pd

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
#from django.utils import timezone

from sct_annotation.annotations.models import Acquisition, Demographic, Image, LabeledImage


logger = logging.getLogger(__name__)


def _get_acquisition(data):
    row = {i: data[i] for i in ('center', 'study', 'subject', 'scanner')}
    if data.date_of_scan:
        row['date_of_scan'] = data.date_of_scan

    acq, created = Acquisition.objects.get_or_create(**row)

    if created:
        logger.info('CREATED Acquisition %s', str(acq))

    return acq


def _get_demographic(data, acq):
    row = {i: data[i] for i in ('surname', 'family_name', 'gender', 'pathology', 'researcher')}
    row['acquisition'] = acq

    demo, created = Demographic.objects.get_or_create(**row)

    if created:
        logger.info('CREATED Demographic %s', str(demo))

    return demo


def _get_images(data, acq):
    sc_seg = [i for i in str(data.sc_seg).split(', ')]
    gm_seg = [i for i in str(data.gm_seg).split(', ')]
    lesion_seg = [i for i in str(data.lesion_seg).split(', ')]

    for contrast in str(data.contrasts).split(', '):
        row = {}
        root_path = Path(settings.SCT_DATASET_ROOT) / str(acq) / str(contrast)
        row['acquisition'] = acq
        row['contrast'] = contrast
        row['filename'] = root_path / f'{contrast}.nii.gz'
        row['pam50'] = data.pam50
        row['ms_mapping'] = data.ms_mapping
        row['gm_model'] = data.gm_model

        img, created = Image.objects.get_or_create(**row)

        if created:
            logger.info('CREATED Image %s', str(img))

        _get_labeled_img(img, sc_seg, LabeledImage.CORD[0], root_path)
        _get_labeled_img(img, gm_seg, LabeledImage.GM[0], root_path)
        _get_labeled_img(img, lesion_seg, LabeledImage.LESION[0], root_path)


def _get_labeled_img(img, labeled_imgs, prefix, root_path):
    match = [i for i in labeled_imgs if i.startswith(img.contrast)]
    if match:
        files = root_path.glob(f'*{prefix}.nii.gz')
        for file_ in files:
            try:
                author = match[0].split()[1]
            except IndexError:
                author = '()'

            row = {
                'label': prefix,
                'contrast': img,
                'filename': file_,
                'author': author
            }
            labeled_img, created = LabeledImage.objects.get_or_create(**row)
            if created:
                logger.info('CREATED LabeledImage %s', str(labeled_img))

            return labeled_img


def get_mod_time(path):
    """Returns the local time of the modified time of the file or folder"""
    return datetime.fromtimestamp(path.stat().st_mtime)


class Command(BaseCommand):
    help = """Import all the json files into a database"""

    def _collect_data_from_folders(self, root):
        self.stdout.write('Collect folders with nii images')
        images = root.glob('*/*/*.nii.gz')
        subjects = defaultdict(list)
        for image in images:
            subjects[image.parent.parent].append(image.parent)

        for subject, contrasts in subjects.items():
            dataset = subject / 'dataset_description.json'
            try:
                with open(dataset) as fd:
                    data = json.load(fd)
                    data = {k.lower(): v for k, v in data.items()}
                    data['modified_date'] = get_mod_time(dataset)
            except FileNotFoundError:
                center, study, subject_name = subject.name.split('_')
                data = {'center': center, 'study': study, 'subject': subject_name}
            data['path'] = str(subject)
            data['name'] = str(subject.name)
            subject_obj, _ = Subject.objects.get_or_create(**data)

            for contrast in contrasts:
                contrast_image = contrast / ('%s.nii.gz' % contrast.name)
                if contrast_image.is_file():
                    _ = Contrast.objects.get_or_create(subject=subject_obj,
                                                       created_date=get_mod_time(contrast_image),
                                                       contrast=contrast.name,
                                                       nifti_path=str(contrast_image))

    def _collect_data_from_pickle(self, pickle_file):
        self.stdout.write('Updating DB from the pickle file %s' % pickle_file)
        data = pd.read_pickle(pickle_file)
        for _, row in data.iterrows():
            acq = _get_acquisition(row)
            demo = _get_demographic(row, acq)
            _get_images(row, acq)

    def add_arguments(self, parser):
        parser.add_argument('pickle_file', type=str)

    def handle(self, *args, **kwargs):
        root = settings.SCT_DATASET_ROOT
        self._collect_data_from_pickle(kwargs['pickle_file'])
