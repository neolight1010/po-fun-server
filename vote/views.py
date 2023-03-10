from typing import cast
from django.contrib.auth.decorators import login_required
import django.forms as forms

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import HttpResponse
from sample.models import Sample
from user.models import User

from vote.models import Vote


class _VoteViewForm(forms.Form):
    direction = forms.ChoiceField(choices=Vote.Direction.choices)


@login_required
def vote_view(request: HttpRequest, sample_id: int) -> HttpResponse:
    request_data = _VoteViewForm(request.POST)

    if not request_data.is_valid():
        return HttpResponseBadRequest(request_data.errors.as_json())

    sample = Sample.objects.filter(id=sample_id).first()

    if sample is None:
        return HttpResponseBadRequest()

    Vote.objects.create(sample_id=sample_id,
                        direction=request_data.cleaned_data['direction'], user=cast(User, request.user))

    return HttpResponse()
