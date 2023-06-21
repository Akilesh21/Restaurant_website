from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Booking_table(models.Model):
    name = models.CharField(max_length=200)
    no_of_guests = models.IntegerField()
    date = models.DateField()
    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

class Category(models.Model):
    slug = models.SlugField()

    def __str__(self)-> str:
        return self.slug

class Menu_table(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT,default=1)

class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_table_id = models.SmallIntegerField()
    rating = models.SmallIntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menu_table = models.ForeignKey(Menu_table,on_delete=models.CASCADE) 
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = ('menu_table','user')
     