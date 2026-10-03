import uuid
from django.db import models
from vendedores.models import Vendedor


class LinkFormulario(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="links")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token} - {self.vendedor.username}"
