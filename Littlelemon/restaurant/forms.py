from django.forms import ModelForm
from .models import Booking_table,Menu_table

class BookingForm(ModelForm):
    class Meta:
        model = Booking_table
        fields = "__all__"
        