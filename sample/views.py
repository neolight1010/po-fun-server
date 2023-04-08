from typing import Any, cast
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from user.models import User

from .models import Sample, Tag
from .forms.SampleForm import SampleForm


def _get_samples_view(sample_type: Sample.SampleType):
    class View(ListView):
        paginate_by = 6
        queryset = Sample.objects.filter(sample_type=sample_type)
        model = Sample

        def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["sample_type"] = sample_type.value.title()

            return context

    return View


DrumsView = _get_samples_view(Sample.SampleType.DRUM)
MelodicView = _get_samples_view(Sample.SampleType.MELODIC)
PacksView = _get_samples_view(Sample.SampleType.PACK)


@login_required
def upload(request: HttpRequest):
    if request.method == "POST":
        form = SampleForm(request.POST, request.FILES)

        if form.is_valid():
            sample: Sample = form.save(commit=False)
            sample.author = cast(User, request.user)

            sample.save()
            form.save_m2m()

            tags = _create_tags(form.cleaned_data["tags"].split(","))
            sample.tags.set(tags)

            return HttpResponseRedirect(reverse("app:index"))

        return HttpResponseBadRequest(form.errors.as_json(), content_type="application/json")
    else:
        form = SampleForm(label_suffix=":")

    for field in form.fields.values():
        field.label = (field.label or "").lower()

    return render(request, "sample/upload.html", {"form": form})


def _create_tags(tag_names: list[str]) -> list[Tag]:
    tags: list[Tag] = []

    for tag_name in tag_names:
        tag_name = tag_name.strip()

        if not tag_name:
            continue

        tag, _ = Tag.objects.get_or_create(name=tag_name)

        tags.append(tag)

    return tags


class SampleDetailView(DetailView):
    model = Sample

    template_name: str = "sample/detail.html"
