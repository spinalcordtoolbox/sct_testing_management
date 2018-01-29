from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.text import force_text

from . import models


class MissingDatasetFilter(admin.SimpleListFilter):
    title = 'Dataset with missing details'
    parameter_name = 'dataset_details'

    def lookups(self, request, model_admin):
        return (('missing', 'Missing Dataset'),
                ('populated', 'Populated Dataset'))

    def queryset(self, request, queryset):
        if self.value() == 'missing':
            return queryset.filter(dataset_file=False)
        return queryset.filter(dataset_file=True)


class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 0
    fields = ('contrast',
              ('pam50', 'ms_mapping', 'gm_model'),
              'filename',
              'get_edit_link')
    readonly_fields = ('get_edit_link', )
    verbose_name = 'Nifti Contrast'
    verbose_name_plural = 'List of Nifti contrast'

    def get_edit_link(self, obj):
        if obj.pk:
            url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
                          args=[force_text(obj.pk)])
            return mark_safe(f'<a href="{url}">Edit {obj._meta.verbose_name}</a>')
        return mark_safe('Save and Continue editing to create a link')
    get_edit_link.short_description = "Edit Image"
    get_edit_link.allow_tags = True


class DemographicInline(admin.StackedInline):
    model = models.Demographic
    extra = 0


class LabeledImageAdmin(admin.StackedInline):
    model = models.LabeledImage
    extra = 0


@admin.register(models.Acquisition)
class AcquisitionAdmin(admin.ModelAdmin):
    list_display = ('center', 'study', 'subject')
    list_filter = (
        'demographic__pathology',
        'images__contrast',
        'images__ms_mapping',
        'images__gm_model',
        'images__pam50')
    search_fields = ('center', 'study')
    list_select_related = ('demographic',)
    inlines = [
        DemographicInline,
        ImageInline
    ]
    actions = [
        'publish_dataset',
    ]
    save_on_top = True

    def publish_dataset(self, request, queryset):
        return JsonResponse([x.to_dict() for x in queryset], safe=False)
    publish_dataset.short_description = 'Download the dataset of the selected entries'


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('acquisition', 'contrast', 'filename')
    fields = (
        'acquisition',
        ('contrast', 'filename'),
        ('start_coverage', 'end_coverage'),
        ('orientation', 'resolution'),
        ('pam50', 'ms_mapping', 'gm_model')
    )
    list_filter = ('contrast', 'pam50', 'ms_mapping', 'gm_model')
    inlines = [
        LabeledImageAdmin
    ]
