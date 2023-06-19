from rest_framework import serializers
from .models import Booking_table,Category,Menu_table
from decimal import Decimal
# Table Booking serilaizer
class Book_table_Serilaizer(serializers.ModelSerializer):
    class Meta:
        model = Booking_table
        fields = ['id','name','no_of_guests','date']

# Menu Serilaizer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class  Menu_tableSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Menu_table
        fields = ['id','title','price','stock','price_after_tax','category','category_id']
        extra_kwargs = {
            'price':{'min_value':2},
            'inventory':{'min_value':0}
        }
    def calculate_tax(self,product:Menu_table):
        return product.price * Decimal(1.8)