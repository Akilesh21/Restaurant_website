from django.contrib import admin

from .models import Booking_table,Menu_table
# Register your models here.
admin.site.register(Booking_table)
admin.site.register(Menu_table)