from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse

from client.models import CustomUser


def auth(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('n_code')
        password = request.POST.get('phone')
        print(username, password)
        if CustomUser.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('client:home'))
            else:
                print("شماره همراه  یا کدملی اشتباه است")
        else:
            user = CustomUser(username=username, n_code=username)
            user.set_password(password)
            user.save()
            return redirect(reverse('client:home'))

    return render(request, 'auth.html')
