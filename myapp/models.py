from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100,null=False,blank=False,default='Windsor warehouse')
    def _str_(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100,validators=[MinValueValidator(0),MaxValueValidator(1000)])
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True,null=True)
    interested = models.PositiveIntegerField(default=0)
    def refil(self):
        self.stock = self.stock+100
    def __str__(self):
        return self.name

class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]
    company = models.CharField(blank=True,null=True,max_length=50)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20,default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    def _str_(self):
        return self.first_name

class Clientavatar(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.FileField(upload_to="photo/", max_length=300, null=True, blank=True)

class Order(models.Model):
    product =  models.ForeignKey('Product',on_delete=models.CASCADE)
    client = models.ForeignKey('Client',on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=1)
    STATUS_CHOICES = [
        (0, 'order Cancelled'),
        (1, 'order Placed'),
        (2, 'order Shipped'),
        (3, 'order CDelivered'),
    ]
    status_date = models.DateField(default=timezone.now)
    def _str_(self):
        return self.product
    def total_cost(self):
        cost = self.num_units*self.product.price
        return cost