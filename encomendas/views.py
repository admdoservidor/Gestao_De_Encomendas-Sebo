from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from .models import Encomenda
from .forms import EncomendaStatusForm


class EncomendaListView(LoginRequiredMixin, ListView):
    template_name = "encomendas/encomenda_list.html"
    context_object_name = "encomendas"

    def get_queryset(self):
        qs = Encomenda.objects.filter(vendedor=self.request.user).select_related("cliente")
        status = self.request.GET.get("status")
        if status in ("aberta", "fechada", "cancelada"):
            qs = qs.filter(status=status)
        cliente_id = self.request.GET.get("cliente")
        if cliente_id:
            qs = qs.filter(cliente_id=cliente_id)
        return qs.order_by("-criado_em")


class EncomendaUpdateView(LoginRequiredMixin, UpdateView):
    model = Encomenda
    form_class = EncomendaStatusForm
    template_name = "encomendas/encomenda_form.html"
    success_url = reverse_lazy("encomendas:list")

    def get_queryset(self):
        return Encomenda.objects.filter(vendedor=self.request.user)


class ExportCSVView(LoginRequiredMixin, View):
    def get(self, request):
        status = request.GET.get("status", "aberta")
        qs = Encomenda.objects.filter(vendedor=request.user, status=status)
        qs = qs.values("livro_titulo").annotate(qtd=Count("id")).order_by("-qtd")
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = f"attachment; filename=encomendas_{status}.csv"
        resp.write("livro,quantidade\n")
        for row in qs:
            resp.write(f'"{row["livro_titulo"]}",{row["qtd"]}\n')
        return resp
