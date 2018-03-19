from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.text import force_text

from . import models


class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 0
    fields = (
        'contrast', ('pam50', 'ms_mapping', 'gm_model'), 'filename', 'get_edit_link'
    )
    readonly_fields = ('get_edit_link',)
    verbose_name = 'Nifti Contrast'
    verbose_name_plural = 'List of Nifti contrast'

    def get_edit_link(self, obj):
        if obj.pk:
            url = reverse(
                f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
                args=[force_text(obj.pk)],
            )
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


class DataListWidget(forms.TextInput):

    def __init__(self, name, data_list, *args, **kwargs):
        super(DataListWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._data_list = data_list
        self.attrs.update({'list': f'list__{self._name}'})

    def render(self, name, value, attrs=None):
        text_html = super(DataListWidget, self).render(name, value, attrs=attrs)
        data_list = f'<datalist id="list__{self._name}">'
        for item in self._data_list:
            data_list += f'<option value="{item}">'
        data_list += '</datalist>'
        return text_html + data_list


class AcquisitionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AcquisitionForm, self).__init__(*args, **kwargs)
        scanners = models.Acquisition.objects.order_by('scanner').values_list(
            'scanner', flat=True
        ).distinct()
        centers = models.Acquisition.objects.order_by('center').values_list(
            'center', flat=True
        ).distinct()
        self.fields['scanner'].widget = DataListWidget('scanner', scanners)
        self.fields['center'].widget = DataListWidget('center', centers)

    class Meta:
        model = models.Acquisition
        fields = '__all__'


class ImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        contrast = models.Image.objects.order_by('contrast').values_list(
            'contrast', flat=True
        ).distinct()
        self.fields['contrast'].widget = DataListWidget('contrast', contrast)

    class Meta:
        model = models.Image
        fields = '__all__'


@admin.register(models.Acquisition)
class AcquisitionAdmin(admin.ModelAdmin):
    list_display = ('center', 'study', 'session')
    list_filter = (
        'demographic__pathology',
        'images__contrast',
        'images__ms_mapping',
        'images__gm_model',
        'images__pam50',
    )
    search_fields = ('center', 'study', 'session')
    list_select_related = ('demographic',)
    inlines = [DemographicInline, ImageInline]
    actions = ['publish_dataset']
    save_on_top = True
    form = AcquisitionForm

    def publish_dataset(self, request, queryset):
        return JsonResponse([x.to_dict() for x in queryset], safe=False)

    publish_dataset.short_description = 'Download the dataset of the selected entries'


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('acquisition', 'contrast', 'filename')
    list_filter = ('contrast', 'ms_mapping', 'gm_model', 'pam50', 'labeled_images__label')
    list_select_related = ('acquisition',)
    search_fields = ('acquisition__center', 'acquisition__study', 'acquisition__session')
    fields = (
        'acquisition',
        ('contrast', 'filename'),
        ('start_coverage', 'end_coverage'),
        ('orientation', 'resolution'),
        ('pam50', 'ms_mapping', 'gm_model'),
    )
    inlines = [LabeledImageAdmin]
    save_on_top = True
    form = ImageForm
