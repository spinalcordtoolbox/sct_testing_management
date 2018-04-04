from pathlib import Path

from django.core.management.base import BaseCommand
import nibabel

from annotations import models


def get_orientation(image):
    """
    orientation_dic = {
        (0, 1): 'L',
        (0, -1): 'R',
        (1, 1): 'P',
        (1, -1): 'A',
        (2, 1): 'I',
        (2, -1): 'S',
    }
    """

    io_orientation = nibabel.orientations.io_orientation
    return io_orientation(image.hdr.get_best_affine())


def get_resolution_by_orientation(image):
    orientation = get_orientation(image)
    dimension = image.header.dim[4:7]
    res = [0, 0, 0]
    for idx, val in enumerate(orientation):
        res[idx] = dimension[val[0]]
    return '{}x{}x{}'.format(*res)


class Command(BaseCommand):

    @staticmethod
    def update_resolution(rows):
        for image in rows:
            obj = nibabel.load(image)
            image.orientations = get_resolution_by_orientation(obj)
            image.save()

    def handle(self, *args, **kwargs):
        root = Path('/Volumes/sct_testing/large')
        if not root.is_dir():
            raise RuntimeError('The root directory is missing')
        imgs = models.Image.objects.all()
        no_res = imgs.filter(resolution__null=True)

        self.update_resolution(no_res)
