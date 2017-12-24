from django.apps import AppConfig


class AnnotationsConfig(AppConfig):
    name = 'sct_annotation.annotations'
    verbose_name = 'SCT testing dataset'

    def ready(self):
        pass
