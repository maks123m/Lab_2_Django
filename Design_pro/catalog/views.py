from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import CustomRegistrationForm
from .models import UserProfile
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ApplicationForm
from .models import Application


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
    return redirect('home')


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('create_application')
    else:
        form = ApplicationForm()

    return render(request, 'catalog/create_application.html', {'form': form})


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catalog/my_applications.html', {
        'applications': applications
    })


@login_required
def delete_application(request, pk):

    app = get_object_or_404(Application, pk=pk, user=request.user)

    if app.status != 'new':
        messages.error(request, 'Нельзя удалить заявку со статусом «Принято в работу» или «Выполнено».')
        return redirect('my_applications')

    if request.method == 'POST':
        app.delete()
        messages.success(request, 'Заявка успешно удалена.')
        return redirect('my_applications')

    return render(request, 'catalog/confirm_delete.html', {'application': app})
