from django.contrib import admin
from .models import UserProfile
from .models import Category

admin.site.register(Category)
admin.site.register(UserProfile)