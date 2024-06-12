from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from product.models import Product


def pay(request, pk=None):
    products = Product.objects.all()
    if pk:
        if products.filter(id=pk).exists():
            pk = pk
        else:
            pk = 0
    else:
        pk = 0
    return render(request, 'pay.html', {'products': products, 'pk': pk})
