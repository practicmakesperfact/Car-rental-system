from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('rental-history/', views.rental_history, name='rental_history'),
    path('about/', views.about, name='about'),
    path('available-cars/', views.available_cars, name='available_cars'),
    path('locations/', views.locations, name='locations'),
]
