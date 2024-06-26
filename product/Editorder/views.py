from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import pytz
import requests
from product.models import Order, Product
from django.conf import settings

@login_required
@csrf_exempt
def edit_order(request, pk):
    order = get_object_or_404(Order, id=pk, user_id=request.user)

    if request.method == 'POST':
        # تنظیم منطقه زمانی به تهران
        current_time = datetime.now()
        tehran_timezone = pytz.timezone('Asia/Tehran')
        tehran_time = current_time.astimezone(tehran_timezone)
        hour = tehran_time.hour

        selected_time = request.POST.get('time', order.date)
        selected_time = int(selected_time)

        if selected_time <= hour:
            msg = "زمانیکه در نظر گرفتید برای دریافت سوخت از تایم های گذشته است لطفا تایم های پیش رو را انتخاب کنید\n سفارش های هرروز از ساعت ۰۰:۰۰ بازمیشوند  "
            return render(request, 'editorder.html', {'msg': msg, 'order': order})

        full_name = request.POST.get('full_name', order.user.get_full_name())
        product_id = request.POST.get('product', order.product.id)
        quantity = request.POST.get('quantity', order.quantity)
        description = request.POST.get('description', order.description)
        lat = request.POST.get('lat', order.lat)
        lon = request.POST.get('lon', order.lon)

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
            error_message = "خطا در دریافت اطلاعات از سرور نشن"
            return render(request, 'editorder.html', {'error_message': error_message, 'order': order})

        if full_name and product_id and quantity and lat and lon and selected_time:
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
