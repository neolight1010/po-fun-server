from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Sample
from .forms.SampleForm import SampleForm


def get_samples_view(sample_type: Sample.SampleType):
    class View(ListView):
        paginate_by = 6
        queryset = Sample.objects.filter(sample_type=sample_type)
        model = Sample

    return View


DrumsView = get_samples_view(Sample.SampleType.DRUM)
MelodicView = get_samples_view(Sample.SampleType.MELODIC)
PacksView = get_samples_view(Sample.SampleType.PACK)


@login_required
def upload(request: HttpRequest):
    if request.method == "POST":
        form = SampleForm(request.POST, request.FILES)

        if form.is_valid():
            sample = form.save(commit=False)
            sample.author = request.user

            sample.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse("app:index"))
    else:
        form = SampleForm(label_suffix="")

    for field in form.fields.values():
        field.label = (field.label or "").lower()

    return render(request, "sample/upload.html", {"form": form})
