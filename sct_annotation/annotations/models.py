from django.conf import settings
from django.db import models


class Acquisition(models.Model):
    date_of_scan = models.DateField(null=True, blank=True)
    center = models.CharField(max_length=32, null=True, blank=True)
    scanner = models.CharField(max_length=32, null=True, blank=True)
    study = models.CharField(max_length=64, null=True, blank=True)
    session = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f'{self.center} {self.study} {self.session}'

    def to_dict(self):
        return {
            'acquisition': {
                x: getattr(self, x)
                for x in ('date_of_scan', 'scanner', 'center', 'study', 'session')
            },
            'demographic': {
                x: getattr(self.demographic, x)
                for x in (
                    'surname',
                    'family_name',
                    'gender',
                    'date_of_birth',
                    'pathology',
                    'researcher',
                )
            },
            'images': {x.contrast: x.to_dict() for x in self.images.all()},
        }


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

    def to_dict(self):
        return self.acquisition.to_dict()


class Image(models.Model):
    acquisition = models.ForeignKey(
        Acquisition, on_delete=models.CASCADE, related_name='images'
    )
    contrast = models.CharField(max_length=32)
    filename = models.CharField(
        'Relative file name: (/Volumes/sct_testing/large/)', max_length=512
    )
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

    def to_dict(self):
        return {
            'path': os.path.dirname(self.filename),
            'file': os.path.basename(self.filename),
            'contrast': self.contrast,
            'coverage': f'{self.start_coverage}:{self.end_coverage}',
            'orientation': self.orientation,
            'resolution': self.resolution,
            'labeling': [x.to_dict() for x in self.labeled_images.all()],
            'study': {
                'pam50': int(self.pam50),
                'ms_mapping': int(self.ms_mapping),
                'gm_model': int(self.gm_model),
            },
        }


class LabeledImage(models.Model):
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
    filename = models.CharField(
        'Relative file name: (/Volumes/sct_testing/large/)', max_length=512
    )
    author = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f'{self.label} -- {self.contrast}'

    def to_dict(self):
        return {'label': self.label, 'file': self.filename, 'rater': self.author}
