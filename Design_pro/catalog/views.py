from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from .forms import CustomRegisterForm


def index(request):
    return render(request, 'catalog/index.html')


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'catalog/register.html', {'form': form})


def login(request):
    return render(request, 'catalog/login.html')


def profile(request):
    return render(request, 'catalog/profile.html')


def custom_logout(request):
    logout(request)
    return redirect('home')

