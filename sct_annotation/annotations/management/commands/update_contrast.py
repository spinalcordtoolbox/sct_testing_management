import os
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone
import nibabel

from annotations import models


def get_orientation(image):
    orientation_dic = {
        (0, 1): 'L',
        (0, -1): 'R',
        (1, 1): 'P',
        (1, -1): 'A',
        (2, 1): 'I',
        (2, -1): 'S',
    }

    io_orientation = nibabel.orientations.io_orientation
    x, y, z = io_orientation(image.hdr.get_best_affine())
    return orientation_dic[tuple(x)] + orientation_dic[tuple(y)] + orientation_dic[tuple(z)]


def update_resolution(image):
    orientation = get_orientation(image)
    res = [0,0,0]
    for idx, val in enumerate(orientation):
        if val in 'LR':
            pass
        if val in 'PA':
            pass
        if val in 'IS':
            pass
    return '{}x{}x{}'


class Command(BaseCommand):

    def update_resolution(rows):
        for image in row:
            if _is_nifti(image.filename):
                obj = nibabel.load(path)
                image.orientations = get_orientation(image)
                get_resolution(image)

    def handle(self, *args, **kwargs):
        root = Path('/Volumes/sct_testing/large')
        if not root.is_dir():
            raise RuntimeError('The root directory is missing')
        imgs = models.Image.objects.all()
        no_res = imgs.filter(resolution__null=True)

        self.update_resolution(no_res)
