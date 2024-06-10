from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse

from client.models import CustomUser


def auth(request):
    context = {}
    if request.method == 'POST':
        print(1)
        username = request.POST.get('n_code')
        password = request.POST.get('phone')
        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                print(user)
                login(request, user)
                print(4)
                return redirect(reverse('client:home'))
            else:
                print("شماره همراه / ایمیل  یا کلمه عبور اشتباه است")
        else:
            user = CustomUser(username=username)
            user.set_password(password)
            print(username)
            print(password)
            user.save()
            return redirect(reverse('client:home'))
        
    return render(request, 'auth.html')
