from django.db import models

# Create your models here.
class Booking_table(models.Model):
    name = models.CharField(max_length=200)
    no_of_guests = models.IntegerField()
    date = models.DateField()
class Menu_table(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    inventory = models.IntegerField()

