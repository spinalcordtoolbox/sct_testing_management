from pathlib import Path

import logging
import nibabel as nib

from django.conf import settings
from django.db import models


logger = logging.getLogger(__name__)


class FileNameMixin(models.Model):

    OK_FILE = ('OK', 'File is available')
    NO_FILE = ('NA', 'File not available')
    ERR_FILE = ('ERR', 'File error')
    FILESTATE = (OK_FILE, NO_FILE, ERR_FILE)
    img_object = None

    filename = models.CharField(
        'File path',
        max_length=512,
        unique=True,
        help_text=f'path prefix: {settings.SCT_DATASET_ROOT}/'
    )
    filestate = models.CharField(
        'The state of the file',
        max_length=3,
        default='NA',
        choices=FILESTATE
    )

    def validate_filename(self):

        path = str(Path(settings.SCT_DATASET_ROOT) / self.filename)
        if self.img_object:
            return self.img_object

        try:
            self.img_object = nib.load(path)
            self.filestate = self.OK_FILE[0]
            logger.info(f'Path {path} exists')
            return self.img_object
        except FileNotFoundError as err:
            self.filestate = self.NO_FILE[0]
            self.error_msg = str(err)
            logger.warning(err)
            return False
        except Exception as err:
            self.filestate = self.ERR_FILE[0]
            self.error_msg = str(err)
            logger.warning(err)
            return False

    def save(self, *args, **kwargs):
        self.validate_filename()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Acquisition(models.Model):

    date_of_scan = models.DateField(null=True, blank=True)
    center = models.CharField(max_length=32)
    scanner = models.CharField(max_length=32, null=True, blank=True)
    study = models.CharField(max_length=64)
    session = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.center}_{self.study}_{self.session}'

    class Meta:
        unique_together = (('center', 'study', 'session'))


class Demographic(models.Model):
    GENDER = (('M', 'Male'), ('F', 'Female'))
    acquisition = models.OneToOneField(
        Acquisition, on_delete=models.CASCADE, related_name='demographic'
    )
    surname = models.CharField(max_length=64, default='unknown')
    family_name = models.CharField(max_length=64, default='unknown')
    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    pathology = models.CharField(max_length=128, null=True, blank=True)
    researcher = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.surname} {self.family_name} {self.gender} {self.pathology}'


class Image(FileNameMixin):
    COVERAGE_CHOICES=(
        ('Brain','Brain'),
        ('PMJ','PMJ'),
        ('C1','C1'),
        ('C2','C2'),
        ('C3','C3'),
        ('C4','C4'),
        ('C5','C5'),
        ('C6','C6'),
        ('C7','C7'),
        ('T1','T1'),
        ('T2','T2'),
        ('T3','T3'),
        ('T4','T4'),
        ('T5','T5'),
        ('T6','T6'),
        ('T7','T7'),
        ('T8','T8'),
        ('T9','T9'),
        ('T10','T10'),
        ('T11','T11'),
        ('T12','T12'),
        ('L1','L1'),
        ('L2','L2'),
        ('L3','L3'),
        ('','N/A'),
        )
    SAG_CONST = 0
    COR_CONST = 1
    AX_CONST = 2
    PLANE_CONST = {SAG_CONST: 'sag', COR_CONST: 'cor', AX_CONST: 'ax'}
    acquisition = models.ForeignKey(
        Acquisition, on_delete=models.CASCADE, related_name='images'
    )
    contrast = models.CharField(max_length=32)
    start_coverage = models.CharField(max_length=16, choices=COVERAGE_CHOICES, default='')
    end_coverage = models.CharField(max_length=16, choices=COVERAGE_CHOICES, default='')
    orientation = models.CharField(max_length=16, null=True, blank=True)

    # isotropic resolution
    is_isotropic = models.BooleanField(default=False)
    sagittal = models.FloatField(default=1.0)
    corrinal = models.FloatField(default=1.0)
    axial = models.FloatField(default=1.0)

    # study
    pam50 = models.BooleanField(default=False,
                                help_text='Is image used in the generation of PAM50')
    ms_mapping = models.BooleanField(default=False,
                                     help_text='Is image used in mapping MS')
    gm_model = models.BooleanField(default=False,
                                   help_text='Is image used to model gray matter')

    def __str__(self):
        return f'{self.contrast} -- {self.acquisition}'

    @property
    def resolution(self):
        return f'{self.sagittal:4.2f} x {self.corrinal:4.2f} x {self.axial:4.2f}'

    def populate_dimensions(self):
        """Calculate orientation and resolution of the image
        """
        img = self.validate_filename()
        resolution = img.header.get_zooms()
        axes = self.calculate_orientation_axis()
        idxs = [int(x[0]) for x in axes]
        lookup = dict(zip(idxs, resolution))

        self.is_isotropic = round(resolution[0], 5) == round(resolution[1], 5) == round(resolution[2], 5)
        self.sagittal = lookup[self.SAG_CONST]
        self.corrinal = lookup[self.COR_CONST]
        self.axial = lookup[self.AX_CONST]
        self.orientation = self.PLANE_CONST[idxs[2]]

    def calculate_orientation_axis(self):
        img = self.validate_filename()
        return nib.orientations.io_orientation(img.header.get_best_affine())

    def save(self, *args, **kwargs):
        img = self.validate_filename()
        if img:
            self.populate_dimensions()

        super().save(*args, **kwargs)


class LabeledImage(FileNameMixin):
    CORD = ('seg_manual', 'Binary mask of spinal cord')
    GM = ('gmseg_manual', 'Binary mask of gray matter')
    LESION = ('lesion_manual', 'Binary mask of lesions')
    DISC = (
        'labels_disc', 'Single voxel at the posterior tip of each inter-vertebral disc'
    )
    LABELS = (CORD, GM, LESION, DISC)
    contrast = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name='labeled_images'
    )
    label = models.CharField(max_length=16,
                             choices=LABELS,
                             help_text='What type of labeled image')
    author = models.CharField(max_length=64, null=True, blank=True)
    label_needs_correction = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.label} -- {self.contrast}'
