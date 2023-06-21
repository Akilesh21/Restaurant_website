from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Booking_table,Menu_table,Rating,Cart,Order,OrderItem
from .forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.forms.models import model_to_dict
from datetime import datetime
# serializers import
from rest_framework import status
from .serializers import Book_table_Serilaizer,Menu_tableSerializer,RatingSerializer,CartSerializer,OrderItemSerializer,OrderSerializers,UserSerializers
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.core.paginator import Paginator,EmptyPage
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import Group,User

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu_table.objects.all()
    main_data = {'menu':menu_data}
    return render(request,'menu.html',{"main":main_data})
def display_menu_items(request,pk=None):
    if pk is not None:
        menu_item = Menu_table.objects.get(pk=pk)    
    return render(request,'menu_item.html',{"menu_item":menu_item})  
# Serializer
# Booking table api view 
class Book_tView(generics.ListCreateAPIView):
    queryset = Booking_table.objects.all()
    serializer_class = Book_table_Serilaizer
class SingleView(generics.RetrieveUpdateAPIView):
    queryset = Booking_table.objects.all()
    serializer_class = Book_table_Serilaizer  

# Bookings detail

# Menu Item api view 
@api_view(['GET','POST'])

def menu_items(request):
    if request.method == 'GET':
        items = Menu_table.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default =2)
        page = request.query_params.get('page',default =1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if ordering:
            ordering_fields = ordering.split(",") 
            items = items.order_by(*ordering_fields) 
        paginator = Paginator(items,per_page=perpage)    
        try:
            items = paginator.page(number=page) 
        except EmptyPage:
            items = [] 
        serialized_item = Menu_tableSerializer(items,many = True)
        return Response(serialized_item.data) 
    elif request.method == 'POST':
        serialized_item = Menu_tableSerializer(data = request.data)
        serialized_item.is_valid(raise_exception=True) 
        serialized_item.save()
        return Response(serialized_item.data,status=status.HTTP_201_CREATED)    
@api_view([])
# it will show the single item passed in server
def single_item(request,id):
    item = get_object_or_404(Menu_table,pk=id)
    serialized_item = Menu_tableSerializer(item)
    return Response(serialized_item.data)   

class RatingView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.request.method =='GET':
            return []
        return [IsAuthenticated()]

class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")
    
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: #normal customer - no group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): #delivery crew
            return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
        else: #delivery crew or manager
            return Order.objects.all()
    def create(self,request,*args,**kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count() 
        if menuitem_count == 0:
            return Response({"message:":"no item in cart"})
        data  = request.data.copy()
        total = self.get_total_price(self.request.user) 
        data['total'] = total
        data['user'] = self.request.user.id 
        order_Serializer = OrderSerializers(data=data)
        if (order_Serializer.is_valid()):
            order = order_Serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id = item['menuitem_id'],
                    price =  item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()
            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_Serializer.data.copy()
            result['total'] = total
            return Response(order_Serializer.data) 

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all() 
        for item in items.values():
            total +=item['price']   
        return total        


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    
    def update(self,request,*args,**kwargs):
        if self.request.user.groups.count()==0:
            return Response('Not Ok')
        else:
            return super().update(request,*args,**kwargs)

class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerializers(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery Crew')
        items = UserSerializers(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)
