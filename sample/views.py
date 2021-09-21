from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Sample
from .forms.SampleForm import SampleForm

class DrumsView(ListView):
    paginate_by = 6
    queryset = Sample.objects.filter(type=Sample.SampleType.DRUM)
    model = Sample


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

    for field in form.fields:
        form.fields[field].label = form.fields[field].label.lower()

    return render(request, "sample/upload.html", {"form": form})
