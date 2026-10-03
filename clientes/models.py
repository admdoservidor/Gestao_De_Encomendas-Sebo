from django.db import models
from vendedores.models import Vendedor


class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, unique=True)
    favorito = models.BooleanField(default=False)
    vendedores = models.ManyToManyField(Vendedor, related_name="clientes")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

    def whatsapp_link(self, texto="Olá!"):
        from urllib.parse import quote
        tel = "".join(c for c in self.telefone if c.isdigit())
        return f"https://wa.me/{tel}?text={quote(texto)}"


class LivroInteresse(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="interesses")
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=150, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nome}"
