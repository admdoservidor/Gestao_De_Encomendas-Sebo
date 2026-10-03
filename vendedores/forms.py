from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Vendedor


class VendedorCreationForm(UserCreationForm):
    class Meta:
        model = Vendedor
        fields = ("username", "email", "telefone", "cpf")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nome de usuário"}),
            "email": forms.EmailInput(attrs={"placeholder": "voce@email.com"}),
            "telefone": forms.TextInput(attrs={"placeholder": "Ex.: (11) 99999-9999"}),
            "cpf": forms.TextInput(attrs={"placeholder": "Ex.: 123.456.789-00"}),
        }
