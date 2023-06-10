from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Booking_table,Menu_table
from .forms import BookingForm
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