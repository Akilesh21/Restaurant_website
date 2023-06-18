from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Booking_table,Menu_table
from .forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.forms.models import model_to_dict
# serializers import
from .serializers import Book_table_Serilaizer,MenuItemSerializer
from rest_framework import generics
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


# api
# @csrf_exempt
# def book_t(request):
#     if request.method == 'GET':
#         names = Booking_table.objects.all().values()
#         return JsonResponse({"name":list(names)})
#     elif request.method == 'POST':
#         name = request.POST.get('name')
#         no_of_guests = request.POST.get('no_of_guests')
#         date = request.POST.get('date')
#         name = Booking_table(
#             name = name,
#             no_of_guests = no_of_guests,
#             date = date
#         )
#         try:
#             name.save()
#         except IntegrityError:
#             return JsonResponse({'error':'true','message':'required field missing'},status =400)
#         return JsonResponse(model_to_dict(name),status=201)   

# Serializer
# Booking table api view 
class Book_tView(generics.ListCreateAPIView):
    queryset = Booking_table.objects.all()
    serializer_class = Book_table_Serilaizer
class SingleView(generics.RetrieveUpdateAPIView):
    queryset = Booking_table.objects.all()
    serializer_class = Book_table_Serilaizer  

# Menu Item api view 
class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu_table.objects.all()
    serializer_class = MenuItemSerializer
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu_table.objects.all()    
    serializer_class = MenuItemSerializer