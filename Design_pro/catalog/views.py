from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm
from .models import UserProfile
from django.contrib.auth import login as auth_login


def index(request):
    return render(request, 'catalog/index.html')


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                consent=True
            )

            auth_login(request, user)
            return redirect('profile')
    else:
        form = CustomRegistrationForm()

    return render(request, 'catalog/register.html', {'form': form})


def login(request):
    return render(request, 'catalog/login.html')


def profile(request):
    return render(request, 'catalog/profile.html')


def custom_logout(request):
    logout(request)
    return redirect('profile')
