from rest_framework import serializers
from .models import Booking_table, Menu_table
# Table Booking serilaizer
class Book_table_Serilaizer(serializers.ModelSerializer):
    class Meta:
        model = Booking_table
        fields = ['id','name','no_of_guests','date']

# Menu Serilaizer
class  MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu_table
        fields = ['id','title','price','inventory']
        extra_kwargs = {
            'price':{'min_value':2},
            'inventory':{'min_value':0}
        }