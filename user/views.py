from user.models import User

from django.views.generic.detail import DetailView


class UserDetailView(DetailView):
    model = User

    template_name = "user/detail.html"
