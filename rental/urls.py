from django.urls import path
from . import views

urlpatterns = [
    # authentications urls
     path('', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    path('home', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
     path('booking/<int:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('rental-history/', views.rental_history, name='rental_history'),
    path('about/', views.about, name='about'),
    path('locations/', views.locations, name='locations'),
    path('rewards/', views.user_rewards, name='user_rewards'),
    path('rewards/redeem/', views.redeem_rewards,name='redeem_rewards'),
    path('cars/<int:car_id>/add_review/', views.add_review, name='add_review'),
    path('rentals/<str:category>/', views.rental_list, name='rental_list'),
    path("services/", views.services, name="services"),
    # path('profile/', views.profile, name='profile'),
    # path('reviews/', views.reviews, name='reviews'),
    path('location/', views.locations, name='locations'),
    path('payment/process/<int:booking_id>', views.process_payment, name='process_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
