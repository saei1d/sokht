from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from client.models import CustomUser
from product.models import Product
from product.models import Order


@csrf_exempt
def pay(request, pk=None):
    products = Product.objects.all()
    if pk:
        if products.filter(id=pk).exists():
            pk = pk
        else:
            pk = 0
    else:
        pk = 0

    if request.method == 'POST':
        user = CustomUser.objects.get(id = 1)
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        description = request.POST.get('description')
        full_name = request.POST.get('full_name')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')

        if product_id and quantity and lat and lon:
            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity

            order = Order(
                user=user,
                product=product,
                description=description,
                location=full_name,
                date='',
                status='Pending',
                cart=False,
                amount=total_price,
                lat=float(lat),
                lon=float(lon)
            )
            order.save()
            return redirect('order_success')  # این نام URL برای صفحه موفقیت آمیز سفارش است

    return render(request, 'pay.html', {'products': products, 'pk': pk})
