from django.contrib import admin
from .models import LinkFormulario

@admin.register(LinkFormulario)
class LinkFormularioAdmin(admin.ModelAdmin):
    list_display = ("token", "vendedor", "ativo", "criado_em")
    list_filter = ("ativo",)
