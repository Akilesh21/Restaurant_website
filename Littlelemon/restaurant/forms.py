from django.forms import ModelForm
from .models import Booking_table,Menu_table
from django import forms
class BookingForm(ModelForm):
    class Meta:
        model = Booking_table
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

