import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomRegisterForm(forms.Form):
    full_name = forms.CharField(
        label="ФИО",
        max_length=100,
    )
    username = forms.CharField(
        label="Логин",
        max_length=30,
    )
    email = forms.EmailField(
        label="Email",
    )
    password = forms.CharField(
        label="Пароль",
    )
    password2 = forms.CharField(
        label="Повтор пароля",
    )
    consent = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
    )

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', full_name):
            raise ValidationError("ФИО может содержать только кириллические буквы, пробелы и дефис.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError("Логин может содержать только латинские буквы и дефис.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        return user
