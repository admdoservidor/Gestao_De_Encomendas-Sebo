from django.contrib import admin
from django.http import FileResponse
from django.shortcuts import redirect
from django.urls import path, include
from pathlib import Path
from config.settings import BASE_DIR


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    return redirect("login")


def sw_js(request):
    return FileResponse((BASE_DIR / "static" / "js" / "sw.js").open("rb"), content_type="application/javascript")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("sw.js", sw_js, name="sw"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("vendedores.urls")),
    path("", include("formularios.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("clientes/", include("clientes.urls")),
    path("encomendas/", include("encomendas.urls")),
]
