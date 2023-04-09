import django.forms as forms

from sample.models import Sample


class SampleForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", empty_value="", required=False)

    class Meta:
        model = Sample
        fields = ["name", "description", "sample_type", "demo", "sample_file"]
