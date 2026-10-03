from django.urls import path
from .views import SignupView

app_name = "vendedores"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]
