from pathlib import Path

from django.conf import settings
from django.db import models
import nibabel as nib

class FileNameMixin(models.Model):
    OK_FILE = ('OK', 'File is available')
    NO_FILE = ('NA', 'File not available')
    ERR_FILE = ('ERR','File error')
    FILESTATE = (OK_FILE, NO_FILE, ERR_FILE)

    filename = models.CharField(
        'File path: (%s)' % settings.SCT_DATASET_ROOT,
        max_length=512,
        unique=True
    )
    filestate = models.CharField(
        'The state of the file',
        max_length=3,
        default='OK',
        choices=FILESTATE
    )

    def validate_filename(self):
        path = str(Path(settings.SCT_DATASET_ROOT) / self.filename)

        try:
            img = nib.load(path)
            self.filestate = self.OK_FILE[0]
        except FileNotFoundError as err:
            self.filestate = self.NO_FILE[0]
            self.error_msg = str(err)
            return False
        except nib.filebasedimages.ImageFileError as err:
            self.filestate = self.ERR_FILE[0]
            self.error_msg = str(err)
            return False

        return True

    def save(self, *args, **kwargs):
        self.validate_filename()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Acquisition(models.Model):
    date_of_scan = models.DateField(null=True, blank=True)
    center = models.CharField(max_length=32, null=True, blank=True)
    scanner = models.CharField(max_length=32, null=True, blank=True)
    study = models.CharField(max_length=64, null=True, blank=True)
    session = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f'{self.center} {self.study} {self.session}'


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
    acquisition = models.ForeignKey(
        Acquisition, on_delete=models.CASCADE, related_name='images'
    )
    contrast = models.CharField(max_length=32)
    start_coverage = models.CharField(max_length=16, null=True, blank=True)
    end_coverage = models.CharField(max_length=16, null=True, blank=True)
    orientation = models.CharField(max_length=16, null=True, blank=True)
    resolution = models.CharField(max_length=16, null=True, blank=True)
    # study
    pam50 = models.BooleanField(default=False,
                                help_text='Is image used in the generation of PAM50')
    ms_mapping = models.BooleanField(default=False,
                                     help_text='Is image used in mapping MS')
    gm_model = models.BooleanField(default=False,
                                   help_text='Is image used to model gray matter')

    def __str__(self):
        return f'{self.contrast} -- {self.acquisition}'


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

    def __str__(self):
        return f'{self.label} -- {self.contrast}'
