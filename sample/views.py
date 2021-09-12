from django.views.generic.list import ListView
from .models import Sample


class DrumsView(ListView):
    paginate_by = 6
    queryset = Sample.objects.filter(type=Sample.SampleType.DRUM)
    model = Sample
