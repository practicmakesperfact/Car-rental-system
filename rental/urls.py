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
#     path('profile/', views.profile, name='profile'),
#     path('reviews/', views.reviews_list, name='reviews_list'),
#     path('location/', views.location_list, name='location_list'),
#     path('payment/', views.payment, name='payment'),

# authentications urls
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
