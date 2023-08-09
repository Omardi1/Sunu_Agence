from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
User = settings.AUTH_USER_MODEL
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Suite(models.Model):
    city = models.CharField(max_length=100)
    category = models.ForeignKey(
    Category, related_name="products", on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=128, unique=True, default="", db_index=True)
    adress = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='suites/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("suite", kwargs={"slug": self.slug})
    
    
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)    
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    
    
    
    def __str__(self):
        return f"{self.suite.name} ({self.quantity})"  
  
    

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    
    
    def __str__(self):
        return self.user.username  
    
  
    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
            
        self.orders.clear()    
        super().delete(*args, **kwargs)
