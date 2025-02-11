from django.db import models

from apps.account.models import User

# Create your models here.

class Local(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=150, blank=True)
    is_active=models.BooleanField(default=False)
    users = models.ManyToManyField(User, blank=True)
    
    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locals"

    def __str__(self):
        return self.name


class Shift(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    finish_at=models.DateTimeField(auto_now=False)
    created_user_pk=models.CharField(max_length=15)
    created_user_username=models.CharField(max_length=15)
    created_user_email=models.CharField(max_length=15)
    local = models.ForeignKey(Local,on_delete=models.CASCADE, related_name='local_shift')

    class Meta:
        verbose_name = "Shift"
        verbose_name_plural = "Shifts"

    def __str__(self):
        return f'{self.pk}'