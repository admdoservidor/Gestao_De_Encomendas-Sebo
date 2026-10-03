from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import VendedorCreationForm


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = VendedorCreationForm
    success_url = reverse_lazy("login")
