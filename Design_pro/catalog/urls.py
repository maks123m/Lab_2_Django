from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from catalog import views as catalog_views

urlpatterns = [
    path('', catalog_views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('create/', views.create_application, name='create_application'),
    path('my/', views.my_applications, name='my_applications'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
    path('admin/categories/', views.admin_categories, name='admin_categories'),
    path('admin/categories/delete/<int:pk>/', views.admin_category_delete, name='admin_category_delete'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
