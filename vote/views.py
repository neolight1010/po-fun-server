from django.contrib.auth.decorators import login_required
import pydantic

from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import HttpResponse

from vote.models import Vote


class _VoteViewData(pydantic.BaseModel):
    direction: Vote.Direction | None = pydantic.Field(...)


@login_required
def vote_view(request: HttpRequest, sample_id: int) -> HttpResponse:
    try:
        request_data = _VoteViewData(**request.POST)
    except pydantic.ValidationError:
        return HttpResponseBadRequest()
