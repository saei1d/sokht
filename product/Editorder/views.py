from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import pytz
import requests
from django.views.decorators.http import require_POST

from product.models import Order, Product
from django.conf import settings
from django.shortcuts import get_object_or_404

@login_required
@csrf_exempt
def edit_order(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return render(request, 'home.html', {'message': 'Order does not exist.'})

    if request.method == 'POST':
        # تنظیم منطقه زمانی به تهران
        current_time = datetime.now()
        tehran_timezone = pytz.timezone('Asia/Tehran')
        tehran_time = current_time.astimezone(tehran_timezone)
        hour = tehran_time.hour

        selected_time = request.POST.get('time', order.date)
        selected_time = int(selected_time)

        if selected_time == '0':
            selected_time = request.POST.get(order.date)

        elif selected_time <= hour:
            msg = "زمانیکه در نظر گرفتید برای دریافت سوخت از تایم های گذشته است لطفا تایم های پیش رو را انتخاب کنید\n سفارش های هرروز از ساعت ۰۰:۰۰ بازمیشوند  "
            return render(request, 'editorder.html', {'msg': msg, 'order': order})
        product_id = request.POST.get('product', order.product.id)
        quantity = request.POST.get('quantity', order.quantity)

        lat = request.POST.get('lat') if request.POST.get('lat') else order.lat
        lon = request.POST.get('lon') if request.POST.get('lon') else order.lon
        description = request.POST.get('description') if request.POST.get('description') else order.description

        product = Product.objects.get(id=product_id)
        price = float(product.price)
        quantity = int(quantity)
        amount = price * quantity

        api_url = f"https://api.neshan.org/v5/reverse?lat={lat}&lng={lon}"
        headers = {
            'Api-Key': settings.NESHAN_API_KEY
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            location_data = response.json()
            formatted_address = location_data.get('formatted_address', 'آدرسی یافت نشد')
        else:
            msg = "خطا در دریافت اطلاعات از سرور "
            return render(request, 'editorder.html', {'msg': msg, 'order': order})
        if product_id and quantity and lat and lon and selected_time:
            order.product = product
            order.description = description
            order.location = formatted_address
            order.date = selected_time
            order.status = 'pending'
            order.cart = False
            order.quantity = quantity
            order.amount = amount
            order.lat = lat
            order.lon = lon
            order.save()
            return redirect('order')

        msg = "مقادیر را با دقت پر کنید لطفا"
        return render(request, 'editorder.html', {'msg': msg, 'order': order})

    products = Product.objects.all()
    return render(request, 'editorder.html', {'order': order, 'products': products})


@require_POST
def delete_order(request, pk):
    print(1)
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('pay')
