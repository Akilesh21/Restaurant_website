from django.db import models

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
    title = models.CharField(max_length=255)

    def __str__(self)-> str:
        return self.title

class Menu_table(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    inventory = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
