from django.contrib.auth import authenticate
from app.forms import RegisterForm
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import login as login_user


def index(request: HttpRequest):
    return render(request, "app/index.html")


def login(request: HttpRequest):
    return render(request, "app/login.html")


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            raw_password = form.clean_password2()

            user = authenticate(request, username=username, password=raw_password)
            login_user(request, user)

            return redirect("app:index")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})
