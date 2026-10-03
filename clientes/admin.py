from django.contrib import admin
from .models import Cliente, LivroInteresse

class LivroInteresseInline(admin.TabularInline):
    model = LivroInteresse
    extra = 0

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "favorito", "criado_em")
    list_filter = ("favorito",)
    search_fields = ("nome", "telefone")
    inlines = [LivroInteresseInline]
