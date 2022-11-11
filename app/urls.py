from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.register, name="register"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
