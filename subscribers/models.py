from django.db import models


# Create your models here.


class Subscriber(models.Model):
    """A subscriber model"""
    email = models.CharField(blank=False, null=False, help_text="Email address", max_length=100)
    full_name = models.CharField(max_length=100, blank=False, null=False, help_text="First name and Last name")

    def __str__(self):
        """string representation"""
        return self.full_name

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
