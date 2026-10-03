from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from encomendas.models import Encomenda
from .models import Cliente
from .forms import ClienteForm


class VendedorQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Cliente.objects.filter(vendedores=self.request.user).prefetch_related("interesses")


class ClienteListView(VendedorQuerysetMixin, ListView):
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(tem_aberta=Exists(
            Encomenda.objects.filter(cliente=OuterRef("pk"), vendedor=self.request.user, status="aberta")
        ))
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(nome__icontains=q) | Q(telefone__icontains=q))
        if self.request.GET.get("favorito") == "1":
            qs = qs.filter(favorito=True)
        return qs


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:list")

    def form_valid(self, form):
        resp = super().form_valid(form)
        self.object.vendedores.add(self.request.user)
        return resp


class ClienteUpdateView(VendedorQuerysetMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:list")

    def get_queryset(self):
        return Cliente.objects.filter(vendedores=self.request.user)


class ClienteDeleteView(VendedorQuerysetMixin, DeleteView):
    model = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("clientes:list")

    def get_queryset(self):
        return Cliente.objects.filter(vendedores=self.request.user)


@login_required
def toggle_favorito(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, vendedores=request.user)
    cliente.favorito = not cliente.favorito
    cliente.save()
    return redirect("clientes:list")
