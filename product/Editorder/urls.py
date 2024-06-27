from django.urls import path

from product.Editorder import views


urlpatterns = [
    path('editorder/<int:pk>/', views.edit_order, name='edit'),
    path('deleted/<int:pk>/', views.delete_order, name='delete'),
]
