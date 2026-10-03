from django.urls import path
from . import views

app_name = "encomendas"

urlpatterns = [
    path("", views.EncomendaListView.as_view(), name="list"),
    path("<int:pk>/editar/", views.EncomendaUpdateView.as_view(), name="update"),
    path("export/csv/", views.ExportCSVView.as_view(), name="export"),
]
