from django.db import models
from clientes.models import Cliente
from vendedores.models import Vendedor


class Encomenda(models.Model):
    class Status(models.TextChoices):
        ABERTA = "aberta", "Aberta"
        FECHADA = "fechada", "Fechada"
        CANCELADA = "cancelada", "Cancelada"

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="encomendas")
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="encomendas")
    livro_titulo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["vendedor", "status"])]

    def __str__(self):
        return f"{self.livro_titulo} ({self.status}) - {self.cliente.nome}"
