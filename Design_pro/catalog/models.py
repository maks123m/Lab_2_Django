from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(
        max_length=150,
        verbose_name='ФИО'
    )
    consent = models.BooleanField(
        default=False,
        verbose_name='Согласие на обработку персональных данных'
    )

    def __str__(self):
        return f'{self.full_name} ({self.user.username})'