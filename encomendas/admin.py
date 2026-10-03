from django.contrib import admin
from .models import Encomenda

@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ("livro_titulo", "cliente", "vendedor", "status", "criado_em")
    list_filter = ("status",)
    search_fields = ("livro_titulo", "cliente__nome")
