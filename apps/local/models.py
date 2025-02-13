from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.account.models import User
from apps.service.models import Service

# Create your models here.


class Client(models.Model):
    email=models.EmailField(max_length=100,unique=True)
    full_name=models.CharField(max_length=150, blank=True)
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.email
    
    @property
    def visit(self):
        return self.client_order.filter(is_paid=True).count()

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


class Order(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    created_user_pk=models.CharField(max_length=15)
    created_user_username=models.CharField(max_length=100)
    created_user_email=models.CharField(max_length=100)
    client_car_plaque=models.CharField(max_length=20)
    client_car_brand=models.CharField(max_length=30,blank=True)
    client_car_model=models.CharField(max_length=50,blank=True)
    local = models.ForeignKey(Local,on_delete=models.CASCADE, related_name='local_order')
    price = models.FloatField(default=0,validators=[MinValueValidator(0)])
    discount = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_paid= models.BooleanField(default=False)
    image = models.ImageField(upload_to='order_image/')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True , blank=True ,related_name='client_order')
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f'{self.pk}'
    
    @property
    def total_price(self):
        items = sum(item.price for item in self.order_item.all()) or 0
        extra = sum(item.price for item in self.order_extra_item.all()) or 0
        if self.discount > 0:
            return round((items + extra)-((items + extra)* self.discount / 100),2)
        return round(items + extra,2)
    
    @property
    def total_items(self):
        return self.order_item.all().count() + self.order_extra_item.all().count()
    
    @property
    def paid(self):
        if self.client_car_plaque and self.total_items > 0:
            return True
        return False
    
class Item(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_item')
    service=models.ForeignKey(Service,on_delete=models.CASCADE, related_name='service_item')
    price = models.FloatField(default=0,validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f'{self.pk}'

class ExtraItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_extra_item')
    description=models.TextField()
    price = models.FloatField(default=1,validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Extra Item"
        verbose_name_plural = "Extra Items"

    def __str__(self):
        return f'{self.pk}'