from django.urls import path

from client import views

urlpatterns = [
    path("auth/",views.auth,name="auth")
]

