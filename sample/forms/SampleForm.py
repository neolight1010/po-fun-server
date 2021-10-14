from django.forms import ModelForm
from sample.models import Sample


class SampleForm(ModelForm):
    class Meta:
        model = Sample
        fields = ["name", "description", "type", "demo", "file"]
