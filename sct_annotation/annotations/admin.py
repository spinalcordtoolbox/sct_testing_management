from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.text import force_text

from . import models
from .serializers import AcquisitionSerializer


class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 0
    fields = (
        ('contrast', 'filename'),
        ('pam50', 'ms_mapping', 'gm_model'),
        'get_edit_link'
    )
    readonly_fields = ('get_edit_link',)

    def get_edit_link(self, obj):
        if obj.pk:
            url = reverse(
                f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
                args=[force_text(obj.pk)],
            )
            return mark_safe(f'<a href="{url}">Edit {obj.filename}</a>')

        return mark_safe('Save and Continue editing to create a link')

    get_edit_link.short_description = "Edit Image"
    get_edit_link.allow_tags = True
    can_delete = False


class DemographicInline(admin.StackedInline):
    model = models.Demographic
    extra = 0
    can_delete = False


class DataListWidget(forms.TextInput):

    def __init__(self, name, data_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)
        contrast = models.Image.objects.order_by('contrast').values_list(
            'contrast', flat=True
        ).distinct()
        self.fields['contrast'].widget = DataListWidget('contrast', contrast)

    class Meta:
        model = models.Image
        fields = '__all__'


class LabeledImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        author = models.LabeledImage.objects.order_by('author').values_list(
            'author', flat=True
        ).distinct()
        self.fields['author'].widget = DataListWidget('author', author)

    class Meta:
        model = models.LabeledImage
        fields = '__all__'


class LabeledImageAdmin(admin.StackedInline):
    model = models.LabeledImage
    fields = ('label', 'filename', 'filestate', 'author','label_needs_correction')
    readonly_fields = ('filestate',)
    extra = 0
    can_delete = False
    form = LabeledImageForm


@admin.register(models.Acquisition)
class AcquisitionAdmin(admin.ModelAdmin):
    fields = ('session', ('center', 'study'), ('date_of_scan', 'scanner'))
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
    inlines = [ImageInline, DemographicInline]
    actions = ['publish_dataset']
    save_on_top = True
    form = AcquisitionForm

    def publish_dataset(self, request, queryset):
        serializer = AcquisitionSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    publish_dataset.short_description = 'Download the json file of the selected entries'


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('acquisition', 'contrast', 'filename')
    list_filter = ('contrast', 'ms_mapping', 'gm_model', 'pam50', 'labeled_images__label',
    'labeled_images__label_needs_correction','start_coverage','end_coverage')
    list_select_related = ('acquisition',)
    search_fields = ('acquisition__center', 'acquisition__study', 'acquisition__session')
    fieldsets = ((None, {'fields':
                         (('acquisition', 'goto_acquisition'),
                          'contrast',
                          'filename',
                          'filestate')}),
                 ('Image structure', {'fields':
                                      ('start_coverage',
                                       'end_coverage',
                                       'orientation',
                                       'get_resolution',
                                       'is_isotropic')}),
                 ('Type of studies', {'fields': (('pam50', 'ms_mapping', 'gm_model'),)}), )
    readonly_fields = ('filestate', 'goto_acquisition', 'get_resolution')
    inlines = [LabeledImageAdmin]
    save_on_top = True
    form = ImageForm

    def goto_acquisition(self, obj):
        if obj.acquisition:
            url = reverse(f'admin:annotations_acquisition_change', args=[force_text(obj.acquisition.pk)])
            return mark_safe(f'<a href="{url}">Click here</a>')
        return ''

    goto_acquisition.short_description = 'Goto to Acquisition form'
    goto_acquisition.allow_tags = True

    def get_resolution(self, obj):
        return mark_safe(obj.resolution)
    get_resolution.short_description = 'Resolution (sag, cor, ax)'
    get_resolution.allow_tags = True
