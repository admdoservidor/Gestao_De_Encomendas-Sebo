from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from clientes.models import Cliente, LivroInteresse
from encomendas.models import Encomenda
from .models import LinkFormulario
from .forms import PedidoPublicoForm


class PedidoCreateView(FormView):
    template_name = "formularios/pedido_form.html"
    form_class = PedidoPublicoForm

    def dispatch(self, request, *args, **kwargs):
        self.link = get_object_or_404(LinkFormulario, token=kwargs["token"], ativo=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["vendedor"] = self.link.vendedor
        return ctx

    def form_valid(self, form):
        nome = form.cleaned_data["nome"]
        telefone = form.cleaned_data["telefone"]
        titulo = form.cleaned_data["livro"]
        autor = form.cleaned_data.get("autor", "")

        cliente, created = Cliente.objects.get_or_create(
            telefone=telefone, defaults={"nome": nome}
        )
        if not created and not cliente.nome and nome:
            cliente.nome = nome
            cliente.save()
        cliente.vendedores.add(self.link.vendedor)

        LivroInteresse.objects.create(cliente=cliente, titulo=titulo, autor=autor)
        Encomenda.objects.create(
            cliente=cliente, vendedor=self.link.vendedor,
            livro_titulo=titulo, status=Encomenda.Status.ABERTA,
        )
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse
        return reverse("formularios:sucesso", kwargs={"token": self.link.token})


class PedidoSucessoView(TemplateView):
    template_name = "formularios/pedido_sucesso.html"
