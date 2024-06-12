from django.urls import path, include


urlpatterns = [
    path('', include('product.order.urls')),
]
