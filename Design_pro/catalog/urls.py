from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('create/', views.create_application, name='create_application'),
    path('my/', views.my_applications, name='my_applications'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),
]
