from django.urls import path
from .views import DrumsView, upload

app_name = "sample"
urlpatterns = [
    path("drums/", DrumsView.as_view(template_name="sample/drums.html"), name="drums"),
    path("upload/", upload, name="upload")
]
