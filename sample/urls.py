from django.urls import path
from .views import DrumsView, MelodicView, PacksView, upload

app_name = "sample"
urlpatterns = [
    path("drums/", DrumsView.as_view(template_name="sample/samples.html"), name="drums"),
    path("melodic/", MelodicView.as_view(template_name="sample/samples.html"), name="melodic"),
    path("packs/", PacksView.as_view(template_name="sample/samples.html"), name="packs"),
    path("upload/", upload, name="upload")
]
