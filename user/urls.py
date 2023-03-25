from django.urls import URLPattern, path

from user.views import UserDetailView


app_name = "user"
urlpatterns: list[URLPattern] = [
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail")
]
