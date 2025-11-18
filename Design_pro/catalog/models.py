from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ\- ]+$',
                message='ФИО должно содержать только кириллические буквы, дефис и пробелы.'
            )
        ],
        verbose_name='ФИО'
    )
    consent = models.BooleanField(
        default=False,
        verbose_name='Согласие на обработку персональных данных'
    )

    def __str__(self):
        return f'{self.full_name} ({self.user.username})'