from django.contrib.auth.models import AbstractUser
from django.db import models


class Vendedor(AbstractUser):
    telefone = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.telefone})"
