import base64
import io

import qrcode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
from clientes.models import Cliente
from encomendas.models import Encomenda
from formularios.models import LinkFormulario


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["total_clientes"] = Cliente.objects.filter(vendedores=user).count()
        ctx["abertas"] = Encomenda.objects.filter(vendedor=user, status="aberta").count()
        ctx["ultimas"] = Encomenda.objects.filter(vendedor=user).select_related("cliente").order_by("-criado_em")[:10]
        return ctx


class LinkView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/links.html"

    def get_link(self):
        link, _ = LinkFormulario.objects.get_or_create(vendedor=self.request.user, ativo=True)
        # desativa extras antigos, mantém só o atual
        LinkFormulario.objects.filter(vendedor=self.request.user).exclude(pk=link.pk).update(ativo=False)
        return link

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        link = self.get_link()
        url = self.request.build_absolute_uri(
            reverse("formularios:pedido", kwargs={"token": link.token})
        )
        ctx["link"] = link
        ctx["form_url"] = url
        ctx["qr_data"] = self.make_qr(url)
        return ctx

    def make_qr(self, url):
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
