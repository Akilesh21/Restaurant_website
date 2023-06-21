from django.contrib import admin

from .models import Booking_table,Menu_table,Category,Rating
# Register your models here.
admin.site.register(Booking_table)
admin.site.register(Menu_table)
admin.site.register(Category)
admin.site.register(Rating)
