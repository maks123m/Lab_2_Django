from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms

from .forms import CustomRegistrationForm, ApplicationForm
from .models import UserProfile, Application, Category


def home(request):
    completed_applications = Application.objects.filter(
        status='completed'
    ).select_related('category').order_by('-created_at')[:4]
    in_progress_count = Application.objects.filter(status='in_progress').count()
    return render(request, 'catalog/index.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })


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


@login_required
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
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'catalog/create_application.html', {'form': form})


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user)

    status_filter = request.GET.get('status')
    if status_filter in ['new', 'in_progress', 'completed']:
        applications = applications.filter(status=status_filter)

    applications = applications.order_by('-created_at')

    return render(request, 'catalog/my_applications.html', {
        'applications': applications,
        'current_status': status_filter,
    })


@login_required
def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if app.status != 'new':
        return redirect('my_applications')

    if request.method == 'POST':
        app.delete()
        return redirect('my_applications')

    return render(request, 'catalog/confirm_delete.html', {'application': app})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}
        labels = {'name': 'Название категории'}


@login_required
def admin_categories(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(request, 'catalog/admin_categories.html', {
        'form': form,
        'categories': categories,
    })


@login_required
def admin_category_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('home')

    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('admin_categories')


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('home')

    applications = Application.objects.exclude(status='completed').order_by('-created_at')

    form_error = None
    target_app_id = None

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        app = get_object_or_404(Application, id=app_id)
        new_status = request.POST.get('status')
        comment = request.POST.get('admin_comment', '').strip()
        design_image = request.FILES.get('design_image')

        if new_status == 'in_progress':
            if not comment:
                form_error = 'comment'
                target_app_id = app.id
        elif new_status == 'completed':
            if not design_image:
                form_error = 'image'
                target_app_id = app.id

        if not form_error:
            if new_status == 'in_progress':
                app.admin_comment = comment
            elif new_status == 'completed':
                app.design_image = design_image
            app.status = new_status
            app.save()
            return redirect('admin_panel')

        return render(request, 'catalog/admin_panel.html', {
            'applications': applications,
            'form_error': form_error,
            'target_app_id': target_app_id,
            'submitted_data': {
                'app_id': app_id,
                'status': new_status,
                'admin_comment': comment,
            }
        })

    return render(request, 'catalog/admin_panel.html', {
        'applications': applications,
    })