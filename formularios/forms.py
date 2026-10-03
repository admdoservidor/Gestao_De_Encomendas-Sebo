from django import forms
from clientes.models import Cliente


class ClienteForm(forms.ModelForm):
    titulo = forms.CharField(
        label="Livro de interesse", required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Dom Casmurro (opcional)"}),
    )
    autor = forms.CharField(
        label="Autor", required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Machado de Assis (opcional)"}),
    )

    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "favorito"]


class PedidoPublicoForm(forms.Form):
    nome = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Seu nome completo"}),
    )
    telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: (11) 99999-9999"}),
    )
    livro = forms.CharField(
        max_length=255, label="Livro de interesse",
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Dom Casmurro"}),
    )
    autor = forms.CharField(
        max_length=150, label="Autor", required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Machado de Assis (opcional)"}),
    )

    def clean_telefone(self):
        tel = "".join(c for c in self.cleaned_data["telefone"] if c.isdigit())
        if len(tel) < 10:
            raise forms.ValidationError("Telefone inválido.")
        return tel
