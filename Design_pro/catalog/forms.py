from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Application

class CustomRegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\- ]+$',
                message='ФИО должно содержать только кириллические буквы, дефис и пробелы.'
            )
        ]
    )
    username = forms.CharField(
        max_length=150,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\-]+$',
                message='Логин может содержать только латинские буквы и дефис.'
            )
        ]
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают.')
        return password_confirm

    def clean_consent(self):
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise ValidationError('Вы должны согласиться на обработку персональных данных.')
        return consent

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'photo': 'Фото помещения (jpg, jpeg, png, bmp, до 2 МБ)',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise ValidationError('Пожалуйста, загрузите фото.')

        allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        ext = photo.name.split('.')[-1].lower()
        if f'.{ext}' not in allowed_extensions:
            raise ValidationError('Недопустимый формат. Разрешены: jpg, jpeg, png, bmp.')


        if photo.size > 2 * 1024 * 1024:
            raise ValidationError('Файл слишком большой. Максимум — 2 МБ.')
        return photo