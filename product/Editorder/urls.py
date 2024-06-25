from django.urls import path

from product.Editorder import views


urlpatterns = [
    path('editorder/', views.editorder, name='edit'),
    ]
