from pathlib import Path
import json

from django.views.decorators.http import require_http_methods
from django.shortcuts import render


@require_http_methods(['GET'])
def annotations(request):
    tests = Path('/Volumes/sct_testing/large')

    directories = [x for x in tests.iterdir() if x.is_dir()]
    datasets = [x.parent for x in tests.glob('*/dataset_description.json')]
    missing_datasets = set(directories) - set(datasets)

    datasets = [(x, 'dataset_element_%d' % i, 'dataset_header_%d' % i)
                for i, x in enumerate(datasets)]
    missing_datasets = [(x, 'dataset_element_%d' % i, 'dataset_header_%d' % i)
                        for i, x in enumerate(missing_datasets)]
    context = {'directories': missing_datasets,
               'datasets': datasets, }

    return render(request, 'annotations/index.html', context)


@require_http_methods(['GET', 'POST'])
def datasets(request, dataset_name):
    tests = Path('/Volumes/sct_testing/large')

    dataset = tests / dataset_name / 'dataset_description.json'
    description = json.load(dataset.open())

    contrasts = tests / dataset_name
    directories = [x for x in contrasts.iterdir() if x.is_dir()]
    segmented = [x.parent for x in contrasts.glob('*/segmentation_description.json')]
    missing_segmentation = set(directories) - set(segmented)

    context = {'description': description,
               'dataset': dataset_name,
               'segmented': segmented,
               'missing_segmentation': missing_segmentation}
    return render(request, 'annotations/dataset_form.html', context)
