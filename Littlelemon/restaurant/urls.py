from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    # Add the remaining URL path configurations here
    path('menu/',views.menu,name="menu"),
    path('menu/<int:pk>/',views.display_menu_items,name="menu_item"),
    path('api/book_t',views.Book_tView.as_view()),
    path('api/book_t/<int:pk>',views.SingleView.as_view()),
    path('api/menu-items',views.menu_items),
    path('api/menu-items/<int:pk>',views.single_item),
    path('ratings',views.RatingView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
]