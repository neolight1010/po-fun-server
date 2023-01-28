from django.urls import path

from . import views

app_name = "vote"
urlpatterns = [path("<int:sample_id>", views.vote_view, name="vote")]
