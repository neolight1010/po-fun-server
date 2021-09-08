from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "app"
urlpatterns = [path("", views.index, name="index"),
               path("login/", auth_views.LoginView.as_view(), name="login"),
               path("register/", views.register, name="register")]
