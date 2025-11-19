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


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', max_length=250)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField('Фото помещения', upload_to='applications/')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']