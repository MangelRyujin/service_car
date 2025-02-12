from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.


class Service(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    price = models.FloatField(default=1,validators=[MinValueValidator(0)])
    

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

   
