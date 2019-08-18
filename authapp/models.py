from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True, verbose_name='аватар')
    age = models.PositiveSmallIntegerField(verbose_name='возраст')
    cellular = models.CharField(max_length=20, blank=True, verbose_name='номер телефона')
