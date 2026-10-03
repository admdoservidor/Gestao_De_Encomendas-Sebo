from django.urls import path
from . import views

app_name = "formularios"

urlpatterns = [
    path("pedido/<uuid:token>/", views.PedidoCreateView.as_view(), name="pedido"),
    path("pedido/<uuid:token>/sucesso/", views.PedidoSucessoView.as_view(), name="sucesso"),
]
