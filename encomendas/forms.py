from django import forms
from encomendas.models import Encomenda


class EncomendaStatusForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ["status"]
