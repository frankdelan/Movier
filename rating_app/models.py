from django.db import models
from django.conf import settings


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')

    year = models.CharField(max_length=4, verbose_name='Year')

    link = models.CharField(max_length=150, verbose_name='Link')

    kp_rating = models.FloatField(verbose_name='KP-Rating')

    rating = models.FloatField(verbose_name='Your rating')

    movie_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user'
    )

    def __str__(self) -> str:
        return f'{self.title}'
